# 支付回调处理完善

> 更新时间：2026-02-14

## 完善概述

本次完善对支付回调处理进行了全面改进，创建了统一的回调处理器模块，提供完整的验证、更新和异常处理机制。

## 完善内容

### 1. 创建统一回调处理器模块

**文件**: `backend/app/payment/callback_handler.py`

#### 1.1 核心类

**PaymentCallbackHandler**: 统一的支付回调处理器
- 提供完整的验证和更新机制
- 支持微信支付和支付宝支付
- 内置防重放攻击保护

#### 1.2 异常类层次

```
PaymentCallbackError (基类)
├── SignatureVerificationError  # 签名验证失败
├── AmountMismatchError         # 金额不匹配
├── PaymentNotFoundError       # 缴费不存在
├── ContractNotFoundError      # 合同不存在
├── DuplicateCallbackError      # 重复回调通知
└── InvalidPaymentStatusError   # 无效的缴费状态
```

### 2. 安全验证机制

#### 2.1 签名验证

- **微信支付**: 使用 `WeChatPayService._verify_sign()`
  - HMAC-SHA256 签名算法
  - 验证回调数据完整性
  - 防止数据被篡改

- **支付宝**: 使用 `AliPayService._verify_sign()`
  - RSA2 签名算法
  - 验证回调数据完整性
  - 防止数据被篡改

#### 2.2 金额验证

```python
def _verify_amount(
    payment: Payment,
    callback_amount: Any,
    amount_type: str = "分"
) -> None:
    """验证支付金额

    - 支持分和元两种单位
    - 允许 0.01 元的误差
    - 验证失败时抛出 AmountMismatchError
    """
```

**验证规则**：
- 微信支付：回调金额单位为"分"，转换为元后比对
- 支付宝：回调金额单位为"元"，直接比对
- 允许误差：0.01 元（1分）

#### 2.3 防重放攻击保护

```python
def _is_duplicate_callback(
    order_no: str,
    notification_id: str
) -> bool:
    """检查是否为重复回调通知

    - 使用内存缓存记录已处理的回调
    - 缓存有效期：5分钟
    - 自动清理过期缓存
    - 检测到重复回调返回 True
    """
```

**缓存机制**：
- 缓存键：`{order_no}:{notification_id}`
- 缓存时间：300 秒（5分钟）
- 自动清理：每次检查时清理过期缓存

### 3. 自动更新机制

#### 3.1 缴费状态更新

```python
async def _update_payment_status(
    payment: Payment,
    transaction_id: str,
    payment_time: Optional[datetime],
    status: int
) -> Payment:
    """更新缴费状态

    - 更新第三方交易号
    - 更新支付时间
    - 更新缴费状态
    - 更新修改时间
    """
```

#### 3.2 缴费确认与合同更新

```python
async def _confirm_payment(
    payment: Payment,
    amount: Decimal
) -> Payment:
    """确认缴费并更新合同

    1. 获取合同
    2. 计算课时（如果合同有单价）
    3. 验证缴费和合同状态
    4. 更新缴费状态为"已确认"
    5. 更新合同剩余课时和总课时
    6. 更新合同实收金额
    7. 使用事务确保数据一致性
    """
```

**业务规则**：
- 只有待确认（status=1）的缴费可以确认
- 只有生效（status=1）或完结（status=2）的合同可以确认缴费
- 课时计算：支付金额 ÷ 合同单价
- 合同更新：
  - `remaining_hours += hours`
  - `total_hours += hours`
  - `received_amount += payment.amount`

### 4. 回调处理流程

#### 4.1 微信支付回调处理

```python
async def handle_wechat_callback(
    notify_data: Dict[str, Any],
    wechat_service: WeChatPayService
) -> str:
    """处理微信支付回调

    1. 验证签名
    2. 提取回调数据
    3. 检查是否重复回调
    4. 获取缴费
    5. 验证金额
    6. 解析支付时间
    7. 判断交易状态并处理
    8. 返回响应（XML格式）
    """
```

**交易状态处理**：
- `SUCCESS`: 支付成功
  - 更新缴费状态为"已确认"
  - 自动确认缴费（增加合同课时）
- `REFUND`: 转入退款
  - 更新缴费状态为"已退款"
- `NOTPAY`, `CLOSED`, `REVOKED`, `PAYERROR`: 不处理

#### 4.2 支付宝回调处理

```python
async def handle_alipay_callback(
    notify_data: Dict[str, Any],
    alipay_service: AliPayService
) -> str:
    """处理支付宝回调

    1. 验证签名
    2. 提取回调数据
    3. 检查是否重复回调
    4. 获取缴费
    5. 验证金额
    6. 解析支付时间
    7. 判断交易状态并处理
    8. 返回响应（文本格式）
    """
```

**交易状态处理**：
- `TRADE_SUCCESS`: 交易支付成功
  - 更新缴费状态为"已确认"
  - 自动确认缴费（增加合同课时）
- `TRADE_FINISHED`: 交易结束
  - 更新缴费状态为"已确认"
- `TRADE_CLOSED`: 交易关闭
- `WAIT_BUYER_PAY`: 等待买家付款

### 5. 便捷函数

```python
async def handle_payment_callback(
    payment_method: int,
    notify_data: Dict[str, Any],
    session: AsyncSession,
    wechat_service: Optional[WeChatPayService] = None,
    alipay_service: Optional[AliPayService] = None
) -> str:
    """处理支付回调的便捷函数

    根据支付方式（payment_method）选择对应的回调处理器

    Args:
        payment_method: 支付方式（1:微信 2:支付宝）
        notify_data: 回调数据
        session: 数据库会话
        wechat_service: 微信支付服务（微信支付必填）
        alipay_service: 支付宝服务（支付宝必填）

    Returns:
        str: 成功响应

    Raises:
        ValueError: 参数错误
    """
```

### 6. API 端点更新

#### 6.1 微信支付回调端点

**文件**: `backend/app/api/v1/payment/wechat.py`

```python
@router.post("/notify", tags=["WeChat Pay"])
async def wechat_pay_notify(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """微信支付回调通知

    使用统一的 PaymentCallbackHandler 处理器
    """
    # 1. 获取回调数据
    xml_data = await request.body()

    # 2. 解析XML为字典
    root = ET.fromstring(xml_data)
    notify_data = {child.tag: child.text for child in root}

    # 3. 使用统一的回调处理器
    response = await handle_payment_callback(
        payment_method=1,  # 微信支付
        notify_data=notify_data,
        session=db,
        wechat_service=wechat_pay_service,
    )

    # 4. 返回响应
    return {"data": response}
```

#### 6.2 支付宝回调端点

**文件**: `backend/app/api/v1/payment/alipay.py`

```python
@router.post("/notify", tags=["AliPay"])
async def alipay_notify(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, str]:
    """支付宝支付回调通知

    使用统一的 PaymentCallbackHandler 处理器
    """
    # 1. 获取回调数据（表单格式）
    form_data = await request.form()

    # 2. 转换为字典
    form_dict = dict(form_data)

    # 3. 使用统一的回调处理器
    response = await handle_payment_callback(
        payment_method=2,  # 支付宝
        notify_data=form_dict,
        session=db,
        alipay_service=alipay_service,
    )

    # 4. 返回响应
    return {"data": response}
```

### 7. 日志记录

#### 7.1 日志级别

- **INFO**: 正常业务流程
  - 回调接收
  - 数据解析
  - 状态更新
  - 缴费确认

- **WARNING**: 异常情况
  - 重复回调
  - 未知的交易状态
  - 合同单价未设置

- **ERROR**: 错误情况
  - 签名验证失败
  - 金额不匹配
  - 缴费/合同不存在
  - 数据库操作失败

#### 7.2 日志内容

```python
# 回调接收
logger.info(
    f"解析微信支付回调: order_no={order_no}, "
    f"transaction_id={transaction_id}, "
    f"trade_state={trade_state}"
)

# 缴费更新
logger.info(
    f"缴费状态更新成功: id={payment.id}, "
    f"payment_no={payment.payment_no}, status={status}"
)

# 缴费确认
logger.info(
    f"缴费确认成功: payment_id={payment.id}, hours={hours}, "
    f"contract_remaining_hours={contract.remaining_hours}"
)

# 重复回调
logger.warning(f"检测到重复回调: {cache_key}")

# 签名验证失败
logger.error(f"处理微信支付回调失败: {e}")
```

### 8. 错误处理

#### 8.1 异常处理策略

```python
try:
    # 1. 验证签名
    handler._verify_wechat_signature(wechat_service, notify_data)

    # 2. 处理回调
    # ...

except SignatureVerificationError as e:
    # 签名验证失败
    logger.error(f"签名验证失败: {e}")
    return wechat_service.build_fail_response("签名验证失败")

except PaymentCallbackError as e:
    # 其他回调处理错误
    logger.error(f"处理回调失败: {e}")
    return wechat_service.build_fail_response(str(e))

except Exception as e:
    # 未预期的错误
    logger.error(f"处理回调失败: {e}", exc_info=True)
    return wechat_service.build_fail_response("处理失败")
```

#### 8.2 响应格式

- **微信支付**: XML 格式
  - 成功: `<xml><return_code><![CDATA[SUCCESS]]></return_code></xml>`
  - 失败: `<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[错误消息]]></return_msg></xml>`

- **支付宝**: 文本格式
  - 成功: `success`
  - 失败: `fail`

### 9. 数据库事务

```python
try:
    # 更新缴费
    await PaymentCRUD.update(payment, self.session)

    # 更新合同
    await ContractCRUD.update(contract, self.session)

    logger.info(f"缴费确认成功")

except IntegrityError as e:
    # 回滚事务
    await self.session.rollback()
    logger.error(f"确认缴费失败: {e}")
    raise PaymentCallbackError(f"确认缴费失败: {str(e)}")
```

### 10. 单元测试

**文件**: `backend/tests/test_payment_callback_handler.py`

#### 10.1 测试类

- `TestPaymentCallbackHandler`: 测试 PaymentCallbackHandler 类
  - 初始化测试
  - 重复回调检测
  - 签名验证
  - 金额验证
  - 获取缴费/合同

- `TestHandlePaymentCallback`: 测试便捷函数
  - 微信支付回调
  - 支付宝回调
  - 参数验证

- `TestCallbackHandlerIntegration`: 集成测试
  - 重复回调保护
  - 缓存过期
  - 缓存清理

#### 10.2 运行测试

```bash
# 运行所有测试
pytest backend/tests/test_payment_callback_handler.py -v

# 运行特定测试
pytest backend/tests/test_payment_callback_handler.py::TestPaymentCallbackHandler -v

# 查看测试覆盖率
pytest backend/tests/test_payment_callback_handler.py --cov=app/payment/callback_handler --cov-report=html
```

## 技术特点

### 1. 统一处理

- 单一的回调处理器类
- 统一的异常层次
- 一致的接口设计
- 标准化的日志格式

### 2. 安全验证

- 完整的签名验证机制
- 严格的金额验证
- 防重放攻击保护
- 详细的审计日志

### 3. 自动化

- 支付成功后自动更新缴费状态
- 自动计算课时（基于合同单价）
- 自动更新合同剩余课时和实收金额
- 事务保证数据一致性

### 4. 容错性

- 完整的异常处理
- 优雅的错误响应
- 防止重复通知
- 允许金额误差

### 5. 可维护性

- 清晰的代码结构
- 详细的注释文档
- 全面的单元测试
- 易于扩展

## 使用示例

### 处理微信支付回调

```python
from app.payment import handle_payment_callback, wechat_pay_service
from app.core.db import get_db

@router.post("/wechat/notify")
async def wechat_notify(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    # 获取回调数据
    xml_data = await request.body()

    # 解析XML
    root = ET.fromstring(xml_data)
    notify_data = {child.tag: child.text for child in root}

    # 处理回调
    response = await handle_payment_callback(
        payment_method=1,  # 微信支付
        notify_data=notify_data,
        session=db,
        wechat_service=wechat_pay_service,
    )

    return {"data": response}
```

### 处理支付宝回调

```python
from app.payment import handle_payment_callback, alipay_service
from app.core.db import get_db

@router.post("/alipay/notify")
async def alipay_notify(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    # 获取回调数据
    form_data = await request.form()
    form_dict = dict(form_data)

    # 处理回调
    response = await handle_payment_callback(
        payment_method=2,  # 支付宝
        notify_data=form_dict,
        session=db,
        alipay_service=alipay_service,
    )

    return {"data": response}
```

## 相关文件

- `backend/app/payment/callback_handler.py` - 回调处理器
- `backend/app/payment/wechat.py` - 微信支付服务
- `backend/app/payment/alipay.py` - 支付宝服务
- `backend/app/api/v1/payment/wechat.py` - 微信支付API
- `backend/app/api/v1/payment/alipay.py` - 支付宝API
- `backend/app/services/payment_service.py` - 缴费服务
- `backend/tests/test_payment_callback_handler.py` - 单元测试

## 变更记录

### 2026-02-14 - 初始实现

- 创建统一的支付回调处理器模块
- 实现签名验证（微信HMAC-SHA256、支付宝RSA2）
- 实现金额验证（支持分和元）
- 实现防重放攻击保护（内存缓存）
- 实现支付成功后自动更新缴费和合同
- 实现完整的异常处理和日志记录
- 更新微信和支付宝API回调端点
- 创建单元测试
- 更新payment模块导出

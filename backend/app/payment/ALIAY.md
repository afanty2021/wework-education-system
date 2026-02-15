# 支付宝支付功能实现总结

## 实现时间
2026-02-14

## 实现内容

### 1. 支付宝支付服务层 (`backend/app/payment/alipay.py`）

**创建的类：**
- `AliPayService` - 支付宝支付服务类

**创建的异常：**
- `AliPayError` - 支付宝异常基类
- `AliPayAPIError` - 支付宝API错误
- `AliPaySignatureError` - 支付宝签名错误
- `AliPayConfigError` - 支付宝配置错误

**实现的功能：**

1. **支付类型支持**
   - 小程序支付（alipay.trade.create）
   - H5支付（alipay.trade.wap.pay）
   - APP支付（alipay.trade.app.pay）
   - 扫码支付（alipay.trade.precreate）

2. **支付订单管理**
   - `create_order()` - 创建统一收单并支付订单
   - `query_order()` - 查询订单状态
   - `close_order()` - 关闭订单

3. **退款管理**
   - `refund()` - 申请退款
   - `query_refund()` - 查询退款状态

4. **回调处理**
   - `parse_notify()` - 解析支付异步通知
   - `parse_refund_notify()` - 解析退款异步通知
   - `build_success_response()` - 构建成功响应
   - `build_fail_response()` - 构建失败响应

5. **签名功能**
   - `_generate_sign()` - 生成RSA2签名
   - `_verify_sign()` - 验证RSA2签名
   - `_build_public_params()` - 构建公共参数

### 2. 支付宝API端点 (`backend/app/api/v1/payment/alipay.py`)

**创建的Pydantic模型：**
- `AliPayOrderCreate` - 支付宝订单创建模型
- `AliPayOrderResponse` - 支付宝订单响应模型
- `AliPayRefundCreate` - 支付宝退款创建模型

**实现的端点：**

1. **订单管理**
   - `POST /api/v1/payment/alipay/create-order` - 创建支付订单
   - `GET /api/v1/payment/alipay/orders/{order_no}` - 查询订单
   - `POST /api/v1/payment/alipay/notify` - 支付异步通知

2. **退款管理**
   - `POST /api/v1/payment/alipay/refund` - 申请退款
   - `GET /api/v1/payment/alipay/refunds/{refund_no}` - 查询退款

### 3. 模块集成

**更新的文件：**
- `backend/app/payment/__init__.py` - 导出支付宝服务
- `backend/app/api/v1/payment/__init__.py` - 注册支付宝路由
- `backend/app/core/config.py` - 添加支付宝配置
- `backend/requirements.txt` - 添加rsa依赖
- `backend/.env.example` - 添加支付宝环境变量

## 技术实现特点

### 1. RSA2签名算法

- 使用2048位RSA密钥
- SHA256哈希算法
- Base64编码
- URL编码传输

**实现方式：**
```python
# 生成签名
import rsa
private_key = rsa.PrivateKey.load_pkcs1(private_key_bytes)
signature = rsa.sign(sign_str.encode('utf-8'), private_key, 'SHA-256')
sign_base64 = base64.b64encode(signature).decode('utf-8')
sign_urlencoded = quote_plus(sign_base64)

# 验证签名
public_key = rsa.PublicKey.load_pkcs1(public_key_bytes)
result = rsa.verify(sign_str.encode('utf-8'), signature, public_key)
```

### 2. 异步HTTP客户端

- 使用httpx异步客户端
- 支持连接池
- 自动重试机制
- 超时控制（30秒）

### 3. 表单格式回调

- 支付宝使用表单格式发送回调
- Content-Type: application/x-www-form-urlencoded
- 自动解析为字典
- 验证签名后处理

### 4. 订单编号规则

- 支付宝订单号：A{timestamp}{contract_id:06d}
- 微信订单号：W{timestamp}{contract_id:06d}
- 退款单号：R{timestamp}{contract_id:06d}

## 业务规则实现

### 1. 订单创建

1. 生成唯一订单号
2. 调用支付宝统一收单API
3. 创建本地缴费记录（status=1，待确认）
4. 返回支付参数

### 2. 支付回调处理

1. 接收表单格式回调数据
2. 验证RSA2签名
3. 解析业务数据
4. 更新本地订单状态
5. 如果支付成功，自动确认缴费（增加课时）
6. 返回success响应

### 3. 退款处理

1. 生成退款单号
2. 调用支付宝退款API
3. 更新订单状态为已退款
4. 扣减合同课时和金额

### 4. 状态流转

**支付状态：**
- 1: 待确认（默认）
- 2: 已确认
- 3: 已退款

**支付宝交易状态：**
- WAIT_BUYER_PAY: 等待买家付款
- TRADE_SUCCESS: 交易支付成功
- TRADE_FINISHED: 交易结束
- TRADE_CLOSED: 交易关闭

## 对比：微信支付 vs 支付宝

| 特性 | 微信支付 | 支付宝支付 |
|------|---------|-----------|
| 签名方式 | HMAC-SHA256 | RSA2 |
| 回调格式 | XML | 表单（form） |
| 订单编号 | W前缀 | A前缀 |
| 金额单位 | 分 | 元 |
| 小程序 | 需要openid | 需要buyer_id |
| 超时 | 默认120秒 | 可配置（30m, 1h等） |
| 测试环境 | 沙箱 | 沙箱 |

## 配置说明

### 环境变量

```bash
# 支付宝配置
ALIPAY_APP_ID=your_app_id
ALIPAY_PRIVATE_KEY=your_private_key
ALIPAY_PUBLIC_KEY=alipay_public_key
ALIPAY_NOTIFY_URL=https://yourdomain.com/api/v1/payment/alipay/notify
ALIPAY_SANDBOX=false
```

### 密钥生成

1. **应用私钥**: 使用支付宝密钥生成工具或OpenSSL生成
2. **应用公钥**: 与私钥配对的公钥，上传到支付宝开放平台
3. **支付宝公钥**: 上传应用公钥后，支付宝返回的公钥

### 回调URL配置

1. 在支付宝开放平台配置回调URL
2. 回调URL必须外网可访问
3. 支持HTTPS（生产环境）和HTTP（开发环境）

## 使用示例

### 小程序支付

```python
# 创建订单
order = await alipay_service.create_order(
    order_no="A1234567890",
    total_amount="100.00",
    subject="课程费用",
    trade_type=AliPayService.TRADE_TYPE_MINI,
    buyer_id="2088xxxxx",
    timeout_express="30m"
)

# 前端调起支付
my.tradePay({
    orderNo: order.order_no
})
```

### H5支付

```python
# 创建订单
order = await alipay_service.create_order(
    order_no="A1234567890",
    total_amount="100.00",
    subject="课程费用",
    trade_type=AliPayService.TRADE_TYPE_MWEB
)

# 前端跳转
window.location.href = order.mweb_url
```

### 扫码支付

```python
# 创建订单
order = await alipay_service.create_order(
    order_no="A1234567890",
    total_amount="100.00",
    subject="课程费用",
    trade_type=AliPayService.TRADE_TYPE_NATIVE
)

# 显示二维码
show_qr_code(order.qr_code)
```

## 错误处理

### 异常层次

```
AliPayError (基类)
├── AliPayConfigError (配置错误)
├── AliPaySignatureError (签名错误)
└── AliPayAPIError (API调用错误)
```

### HTTP状态码

- 400: 数据验证错误
- 404: 资源不存在
- 500: 服务器错误

### 回调响应

- 成功: success
- 失败: fail

## 安全考虑

### 1. 签名验证

- 所有回调通知都验证签名
- 签名使用RSA2算法
- 密钥安全存储

### 2. 数据验证

- 订单号唯一性
- 金额范围验证
- 交易类型验证

### 3. 回调安全

- 验证签名
- 验证来源IP（可选）
- 验证时间戳（可选）

## 测试建议

### 1. 单元测试

创建 `backend/tests/test_alipay.py`：
- 测试签名生成和验证
- 测试XML/表单转换
- 测试工具方法

### 2. 集成测试

- 使用支付宝沙箱环境
- 测试完整支付流程
- 测试退款流程

### 3. 回调测试

- 使用内网穿透工具（ngrok等）
- 模拟支付宝回调
- 验证签名验证

## 代码质量

- **SOLID原则**
  - 单一职责：服务类只负责支付集成
  - 开闭原则：通过异常扩展功能

- **DRY原则**
  - 复用PaymentService业务逻辑
  - 复用公共方法

- **KISS原则**
  - 简洁明了的接口设计
  - 清晰的命名规范

- **YAGNI原则**
  - 只实现当前需要的功能
  - 避免过度设计

## 下一步建议

1. **单元测试**
   - 创建完整的单元测试
   - 测试签名生成和验证
   - 测试回调处理

2. **集成测试**
   - 使用支付宝沙箱环境
   - 测试完整支付流程

3. **日志增强**
   - 添加更详细的日志
   - 记录关键操作

4. **监控告警**
   - 支付成功率监控
   - 回调处理失败告警

## 相关文件

### 核心文件

- `backend/app/payment/alipay.py` - 支付宝支付服务
- `backend/app/api/v1/payment/alipay.py` - 支付宝API端点
- `backend/app/core/config.py` - 配置管理
- `backend/app/models/payment.py` - 支付数据模型
- `backend/app/schemas/payment.py` - 支付Pydantic模型
- `backend/app/services/payment_service.py` - 支付业务逻辑

### 对比文件

- `backend/app/payment/wechat.py` - 微信支付服务
- `backend/app/api/v1/payment/wechat.py` - 微信支付API端点

## 参考资料

- [支付宝统一收单](https://opendocs.alipay.com/open/02e7go)
- [支付宝查询订单](https://opendocs.alipay.com/open/02e7k8)
- [支付宝关闭订单](https://opendocs.alipay.com/open/02e7k7)
- [支付宝申请退款](https://opendocs.alipay.com/open/02e7kt)
- [支付宝支付通知](https://opendocs.alipay.com/open/02e7k6)
- [RSA签名](https://opendocs.alipay.com/open/291/106239)

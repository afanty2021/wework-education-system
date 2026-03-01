[根目录](../../../CLAUDE.md) > [backend](../../) > [app](../) > **payment**

# Payment - 支付模块

> 最后更新：2026-02-16

# 支付宝支付集成

> 最后更新：2026-02-14

## 概述

本模块提供支付宝支付API的完整集成，支持小程序支付、H5支付、APP支付和扫码支付。

## 文件结构

```
payment/
├── __init__.py              # 模块导出（含微信支付和支付宝）
├── wechat.py                # 微信支付服务
└── alipay.py                # 支付宝支付服务

api/v1/payment/
├── __init__.py              # 模块导出
├── wechat.py                # 微信支付API端点
└── alipay.py                # 支付宝支付API端点

tests/
├── test_wechat_pay.py       # 微信支付单元测试
└── test_alipay.py           # 支付宝支付单元测试
```

## 核心功能

### 1. 支付宝支付服务 (AliPayService)

**文件**: `backend/app/payment/alipay.py`

#### 1.1 支付类型

- `TRADE_TYPE_MINI`: 小程序支付 (alipay.trade.create)
- `TRADE_TYPE_MWEB`: H5支付 (alipay.trade.wap.pay)
- `TRADE_TYPE_APP`: APP支付 (alipay.trade.app.pay)
- `TRADE_TYPE_NATIVE`: 扫码支付 (alipay.trade.precreate)

#### 1.2 订单状态

- `TRADE_STATUS_WAIT_BUYER_PAY`: 交易创建，等待买家付款
- `TRADE_STATUS_TRADE_SUCCESS`: 交易支付成功
- `TRADE_STATUS_TRADE_FINISHED`: 交易结束，不可退款
- `TRADE_STATUS_TRADE_CLOSED`: 未付款交易超时关闭

#### 1.3 退款状态

- `REFUND_STATUS_SUCCESS`: 退款成功
- `REFUND_STATUS_FAILED`: 退款失败
- `REFUND_STATUS_PROCESSING`: 退款处理中

#### 1.4 主要方法

**创建订单**:
```python
result = await alipay_service.create_order(
    order_no="A1234567890",
    total_amount="100.00",
    subject="课程费用",
    trade_type=AliPayService.TRADE_TYPE_MINI,
    buyer_id="2088xxxxx",  # 支付宝用户ID
    timeout_express="30m"  # 30分钟超时
)
```

**查询订单**:
```python
result = await alipay_service.query_order(
    order_no="A1234567890"
)
```

**关闭订单**:
```python
result = await alipay_service.close_order(
    order_no="A1234567890"
)
```

**申请退款**:
```python
result = await alipay_service.refund(
    order_no="A1234567890",
    refund_no="R1234567890",
    refund_amount="100.00",
    refund_reason="用户申请退款"
)
```

**查询退款**:
```python
result = await alipay_service.query_refund(
    refund_no="R1234567890"
)
```

#### 1.5 回调处理

**解析支付回调**:
```python
# 表单格式数据
notify_data = alipay_service.parse_notify(form_data)
```

**解析退款回调**:
```python
# 表单格式数据
refund_data = alipay_service.parse_refund_notify(form_data)
```

**构建响应**:
```python
# 成功响应
success_text = alipay_service.build_success_response()  # "success"

# 失败响应
fail_text = alipay_service.build_fail_response()  # "fail"
```

### 2. 支付宝API端点

**文件**: `backend/app/api/v1/payment/alipay.py`

#### 2.1 Pydantic 模型

**AliPayOrderCreate**: 创建支付订单
- `contract_id`: 合同ID
- `amount`: 支付金额（元）
- `subject`: 订单标题
- `trade_type`: 交易类型
- `buyer_id`: 买家支付宝用户ID（小程序支付必填）
- `timeout_express`: 绝对超时时间（格式：30m, 1h, 1d等）
- `total_quantity`: 购买数量
- `operator_id`: 操作员ID
- `store_id`: 商户门店编号
- `attach`: 附加数据

**AliPayOrderResponse**: 支付订单响应
- `order_no`: 商户订单号
- `trade_no`: 支付宝交易号
- `out_trade_no`: 商户订单号
- `total_amount`: 订单金额
- `receipt_amount`: 实收金额
- `buyer_pay_amount`: 买家付款金额
- `point_amount`: 积分金额
- `invoice_amount`: 发票金额
- `send_pay_date`: 交易付款时间
- `code`: 小程序支付码（小程序支付）
- `mweb_url`: H5支付链接（H5支付）
- `qr_code`: 二维码内容（扫码支付）

**AliPayRefundCreate**: 申请退款
- `order_no`: 商户订单号
- `refund_no`: 退款单号
- `refund_amount`: 退款金额（元）
- `refund_reason`: 退款原因
- `out_order_no`: 商户订单号（与order_no二选一）

#### 2.2 API 端点

**创建支付订单**:
```
POST /api/v1/payment/alipay/create-order
```

**支付回调通知**:
```
POST /api/v1/payment/alipay/notify
```

**查询订单**:
```
GET /api/v1/payment/alipay/orders/{order_no}
```

**申请退款**:
```
POST /api/v1/payment/alipay/refund
```

**查询退款**:
```
GET /api/v1/payment/alipay/refunds/{refund_no}
```

## 配置要求

### 环境变量

在 `.env` 文件中配置：

```bash
# 支付宝配置
ALIPAY_APP_ID=your_app_id
ALIPAY_PRIVATE_KEY=your_private_key
ALIPAY_PUBLIC_KEY=alipay_public_key
ALIPAY_NOTIFY_URL=https://yourdomain.com/api/v1/payment/alipay/notify
ALIPAY_SANDBOX=false
```

### 密钥获取

1. **应用ID (ALIPAY_APP_ID)**: 支付宝开放平台创建应用后获取
2. **应用私钥 (ALIPAY_PRIVATE_KEY)**: 使用支付宝密钥生成工具生成
3. **支付宝公钥 (ALIPAY_PUBLIC_KEY)**: 上传应用公钥后，支付宝返回的公钥

### RSA2签名

支付宝使用RSA2签名方式：
- 密钥长度：2048位
- 签名算法：SHA256WithRSA
- 密钥格式：PKCS#1

**生成密钥对**:
```bash
# 使用支付宝密钥生成工具
# 下载地址：https://opendocs.alipay.com/open/291/106239

# 或使用OpenSSL生成
openssl genrsa -out app_private_key.pem 2048
openssl rsa -in app_private_key.pem -pubout -out app_public_key.pem
```

### 回调URL配置

1. 在支付宝开放平台配置回调URL
2. 回调URL必须外网可访问
3. 支持HTTPS（生产环境）和HTTP（开发环境）

## 业务流程

### 1. 创建支付订单流程

```
用户发起支付
    ↓
生成订单号（A{timestamp}{contract_id:06d}）
    ↓
调用支付宝统一收单API
    ↓
创建本地缴费记录
    ↓
返回支付参数
    ↓
前端调起支付
```

### 2. 支付回调处理流程

```
支付宝发送支付通知（表单格式）
    ↓
验证签名（RSA2）
    ↓
解析回调数据
    ↓
更新本地订单状态
    ↓
自动确认缴费（增加课时）
    ↓
返回成功响应（success）
```

### 3. 退款流程

```
用户申请退款
    ↓
生成退款单号
    ↓
调用支付宝退款API
    ↓
更新订单状态为已退款
    ↓
扣减合同课时和金额
```

## 异常处理

### 异常类

- `AliPayError`: 异常基类
- `AliPayAPIError`: API调用错误
- `AliPaySignatureError`: 签名错误
- `AliPayConfigError`: 配置错误

### 错误处理

所有API端点都包含完整的错误处理：
- 配置错误 → HTTP 500
- API错误 → HTTP 500
- 签名错误 → 返回失败响应
- 数据验证错误 → HTTP 400

## 技术特点

### 1. RSA2签名

- 使用2048位RSA密钥
- SHA256哈希算法
- Base64编码签名
- URL编码传输

### 2. 异步HTTP客户端

- 使用httpx异步客户端
- 支持连接池
- 自动重试机制
- 超时控制

### 3. 表单格式回调

- 支付宝使用表单格式发送回调
- application/x-www-form-urlencoded
- 自动解析为字典
- 验证签名后处理

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

# 前端使用返回的code调起支付
my.tradePay({
    orderNo: order.order_no,
    tradeNO: order.trade_no
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

# 前端跳转到支付链接
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

# 前端显示二维码
qr_code_url = order.qr_code
```

## 对比：微信支付 vs 支付宝支付

| 特性 | 微信支付 | 支付宝支付 |
|------|---------|-----------|
| 签名方式 | HMAC-SHA256 | RSA2 |
| 回调格式 | XML | 表单（form） |
| 订单编号 | W前缀 | A前缀 |
| 支付类型 | JSAPI/MWEB/APP/NATIVE | MINI/MWEB/APP/NATIVE |
| 金额单位 | 分 | 元 |
| 小程序 | 需要openid | 需要buyer_id |
| 测试环境 | 沙箱 | 沙箱 |

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

## 相关文件

- `backend/app/core/config.py` - 配置管理
- `backend/app/models/payment.py` - 支付数据模型
- `backend/app/schemas/payment.py` - 支付Pydantic模型
- `backend/app/services/payment_service.py` - 支付业务逻辑
- `backend/app/api/v1/payments.py` - 支付API端点
- `backend/app/payment/wechat.py` - 微信支付服务
- `backend/app/api/v1/payment/wechat.py` - 微信支付API端点
- `backend/tests/test_alipay.py` - 单元测试

## 参考资料

- [支付宝统一收单](https://opendocs.alipay.com/open/02e7go)
- [支付宝查询订单](https://opendocs.alipay.com/open/02e7k8)
- [支付宝关闭订单](https://opendocs.alipay.com/open/02e7k7)
- [支付宝申请退款](https://opendocs.alipay.com/open/02e7kt)
- [支付宝支付通知](https://opendocs.alipay.com/open/02e7k6)
- [RSA签名](https://opendocs.alipay.com/open/291/106239)

## 变更记录

### 2026-02-14 - 初始实现

- 创建支付宝支付服务类
- 实现统一收单、查询、关闭订单
- 实现退款申请和查询
- 实现支付和退款回调处理
- 创建API端点
- 添加RSA2签名支持
- 更新配置文件，添加支付宝配置
- 更新requirements.txt，添加rsa依赖
- 完成到payment模块导出
- 完成到API路由注册


<claude-mem-context>
# Recent Activity

<!-- This section is auto-generated by claude-mem. Edit content outside the tags. -->

### Feb 16, 2026

| ID | Time | T | Title | Read |
|----|------|---|-------|------|
| #4141 | 5:42 AM | ✅ | Updated payment module CLAUDE.md with navigation header | ~165 |
</claude-mem-context>
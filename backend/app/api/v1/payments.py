"""Payments API Routes

缴费管理相关 API 路由
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentUpdate,
    PaymentConfirm,
    PaymentRefund,
)
from app.services.payment_service import (
    PaymentService,
    PaymentNotFoundError,
    PaymentNoExistsError,
    ContractNotFoundError,
    InvalidPaymentDataError,
    InvalidPaymentStatusError,
    PaymentServiceError,
)


router = APIRouter()


@router.get("", response_model=List[PaymentResponse], tags=["Payments"])
async def list_payments(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    contract_id: Optional[int] = Query(None, description="合同ID筛选"),
    status: Optional[int] = Query(None, ge=1, le=3, description="状态筛选 (1:待确认 2:已确认 3:已退款)"),
    payment_method: Optional[int] = Query(None, ge=1, le=5, description="支付方式筛选 (1:微信 2:支付宝 3:现金 4:银行卡 5:转账)"),
) -> List[PaymentResponse]:
    """获取缴费列表

    支持分页、合同筛选、状态筛选和支付方式筛选
    """
    try:
        payments = await PaymentService.get_all_payments(
            session=db,
            skip=skip,
            limit=limit,
            contract_id=contract_id,
            status=status,
            payment_method=payment_method
        )
        return payments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取缴费列表失败: {str(e)}"
        )


@router.get("/stats/count", tags=["Payments"])
async def count_payments(
    db: AsyncSession = Depends(get_db),
    contract_id: Optional[int] = Query(None, description="合同ID筛选"),
    status: Optional[int] = Query(None, ge=1, le=3, description="状态筛选"),
    payment_method: Optional[int] = Query(None, ge=1, le=5, description="支付方式筛选"),
):
    """统计缴费数量"""
    try:
        count = await PaymentService.count_payments(
            session=db,
            contract_id=contract_id,
            status=status,
            payment_method=payment_method
        )
        return {"count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"统计缴费数量失败: {str(e)}"
        )


@router.get("/{payment_id}", response_model=PaymentResponse, tags=["Payments"])
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
) -> PaymentResponse:
    """获取缴费详情"""
    try:
        payment = await PaymentService.get_payment_by_id(payment_id, db)
        return payment
    except PaymentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"缴费不存在: {payment_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取缴费详情失败: {str(e)}"
        )


@router.get("/no/{payment_no}", response_model=PaymentResponse, tags=["Payments"])
async def get_payment_by_no(
    payment_no: str,
    db: AsyncSession = Depends(get_db),
) -> PaymentResponse:
    """根据缴费编号获取缴费详情"""
    try:
        payment = await PaymentService.get_payment_by_no(payment_no, db)
        return payment
    except PaymentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"缴费不存在: {payment_no}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取缴费详情失败: {str(e)}"
        )


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED, tags=["Payments"])
async def create_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
) -> PaymentResponse:
    """创建缴费

    自动验证合同存在性和缴费编号唯一性
    """
    try:
        payment = await PaymentService.create_payment(
            payment_data=payment_data,
            created_by=None,  # TODO: 从认证上下文获取当前用户
            session=db
        )
        return payment
    except ContractNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PaymentNoExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidPaymentDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建缴费失败: {str(e)}"
        )


@router.put("/{payment_id}", response_model=PaymentResponse, tags=["Payments"])
async def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: AsyncSession = Depends(get_db),
) -> PaymentResponse:
    """更新缴费"""
    try:
        payment = await PaymentService.update_payment(
            payment_id=payment_id,
            payment_data=payment_data,
            session=db
        )
        return payment
    except PaymentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"缴费不存在: {payment_id}"
        )
    except InvalidPaymentDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新缴费失败: {str(e)}"
        )


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Payments"])
async def delete_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除缴费

    只有待确认状态的缴费可以删除
    """
    try:
        await PaymentService.delete_payment(payment_id, db)
    except PaymentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"缴费不存在: {payment_id}"
        )
    except InvalidPaymentStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except PaymentServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除缴费失败: {str(e)}"
        )


# ==================== 缴费确认 API ====================

@router.post("/{payment_id}/confirm", response_model=PaymentResponse, tags=["Payments"])
async def confirm_payment(
    payment_id: int,
    confirm_data: PaymentConfirm,
    db: AsyncSession = Depends(get_db),
) -> PaymentResponse:
    """确认缴费

    确认后自动增加合同剩余课时
    """
    try:
        payment = await PaymentService.confirm_payment(
            payment_id=payment_id,
            confirm_data=confirm_data,
            session=db
        )
        return payment
    except PaymentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"缴费不存在: {payment_id}"
        )
    except ContractNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidPaymentStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"确认缴费失败: {str(e)}"
        )


# ==================== 退款 API ====================

@router.post("/{payment_id}/refund", response_model=PaymentResponse, tags=["Payments"])
async def refund_payment(
    payment_id: int,
    refund_data: PaymentRefund,
    db: AsyncSession = Depends(get_db),
) -> PaymentResponse:
    """退款

    扣减合同课时和实收金额
    """
    try:
        payment = await PaymentService.refund_payment(
            payment_id=payment_id,
            refund_data=refund_data,
            session=db
        )
        return payment
    except PaymentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"缴费不存在: {payment_id}"
        )
    except ContractNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidPaymentStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidPaymentDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"退款失败: {str(e)}"
        )

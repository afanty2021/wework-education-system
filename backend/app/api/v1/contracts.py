"""Contracts API Routes

合同管理相关 API 路由
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.contract import (
    ContractCreate,
    ContractResponse,
    ContractUpdate,
    ContractDeductHours,
    ContractAddHours,
)
from app.services.contract_service import (
    ContractService,
    ContractNotFoundError,
    ContractNoExistsError,
    StudentNotFoundError,
    CourseNotFoundError,
    InsufficientHoursError,
    InvalidContractDataError,
    InvalidContractStatusError,
    ContractServiceError,
)


router = APIRouter()


@router.get("", response_model=List[ContractResponse], tags=["Contracts"])
async def list_contracts(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    student_id: Optional[int] = Query(None, description="学员ID筛选"),
    course_id: Optional[int] = Query(None, description="课程ID筛选"),
    status: Optional[int] = Query(None, ge=1, le=4, description="状态筛选 (1:生效 2:完结 3:退费 4:过期)"),
) -> List[ContractResponse]:
    """获取合同列表

    支持分页、学员筛选、课程筛选和状态筛选
    """
    try:
        contracts = await ContractService.get_all_contracts(
            session=db,
            skip=skip,
            limit=limit,
            student_id=student_id,
            course_id=course_id,
            status=status
        )
        return contracts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取合同列表失败: {str(e)}"
        )


@router.get("/expiring", response_model=List[ContractResponse], tags=["Contracts"])
async def list_expiring_contracts(
    db: AsyncSession = Depends(get_db),
    days: int = Query(30, ge=1, le=365, description="预警天数"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
) -> List[ContractResponse]:
    """获取即将到期的合同列表

    支持分页和预警天数设置
    """
    try:
        from app.crud.contract import ContractCRUD

        contracts = await ContractCRUD.get_expiring_contracts(
            session=db,
            days=days,
            skip=skip,
            limit=limit
        )
        return contracts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取即将到期合同列表失败: {str(e)}"
        )


@router.get("/{contract_id}", response_model=ContractResponse, tags=["Contracts"])
async def get_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """获取合同详情"""
    try:
        contract = await ContractService.get_contract_by_id(contract_id, db)
        return contract
    except ContractNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"合同不存在: {contract_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取合同详情失败: {str(e)}"
        )


@router.get("/no/{contract_no}", response_model=ContractResponse, tags=["Contracts"])
async def get_contract_by_no(
    contract_no: str,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """根据合同编号获取合同详情"""
    try:
        contract = await ContractService.get_contract_by_no(contract_no, db)
        return contract
    except ContractNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"合同不存在: {contract_no}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取合同详情失败: {str(e)}"
        )


@router.post("", response_model=ContractResponse, status_code=status.HTTP_201_CREATED, tags=["Contracts"])
async def create_contract(
    contract_data: ContractCreate,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """创建合同

    自动计算总金额，验证学员和课程存在性
    """
    try:
        contract = await ContractService.create_contract(
            contract_data=contract_data,
            created_by=None,  # TODO: 从认证上下文获取当前用户
            session=db
        )
        return contract
    except StudentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ContractNoExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidContractDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建合同失败: {str(e)}"
        )


@router.put("/{contract_id}", response_model=ContractResponse, tags=["Contracts"])
async def update_contract(
    contract_id: int,
    contract_data: ContractUpdate,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """更新合同"""
    try:
        contract = await ContractService.update_contract(
            contract_id=contract_id,
            contract_data=contract_data,
            session=db
        )
        return contract
    except ContractNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"合同不存在: {contract_id}"
        )
    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidContractDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新合同失败: {str(e)}"
        )


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Contracts"])
async def delete_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除合同

    删除前会检查是否有关联的排课记录
    """
    try:
        await ContractService.delete_contract(contract_id, db)
    except ContractNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"合同不存在: {contract_id}"
        )
    except ContractServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除合同失败: {str(e)}"
        )


# ==================== 课时管理 API ====================

@router.post("/{contract_id}/deduct", response_model=ContractResponse, tags=["Contracts"])
async def deduct_contract_hours(
    contract_id: int,
    deduct_data: ContractDeductHours,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """扣减合同课时

    会检查课时是否足够以及合同状态
    """
    try:
        contract = await ContractService.deduct_hours(
            contract_id=contract_id,
            deduct_data=deduct_data,
            session=db
        )
        return contract
    except ContractNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"合同不存在: {contract_id}"
        )
    except InsufficientHoursError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidContractStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"扣减课时失败: {str(e)}"
        )


@router.post("/{contract_id}/add-hours", response_model=ContractResponse, tags=["Contracts"])
async def add_contract_hours(
    contract_id: int,
    add_data: ContractAddHours,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """追加合同课时

    会同时更新总课时和剩余课时
    """
    try:
        contract = await ContractService.add_hours(
            contract_id=contract_id,
            add_data=add_data,
            session=db
        )
        return contract
    except ContractNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"合同不存在: {contract_id}"
        )
    except InvalidContractStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"追加课时失败: {str(e)}"
        )


@router.post("/{contract_id}/expire", response_model=ContractResponse, tags=["Contracts"])
async def mark_contract_as_expired(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """标记合同为过期

    将合同状态更新为过期（4）
    """
    try:
        contract = await ContractService.mark_as_expired(
            contract_id=contract_id,
            session=db
        )
        return contract
    except ContractNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"合同不存在: {contract_id}"
        )
    except InvalidContractStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"标记合同过期失败: {str(e)}"
        )


# ==================== 统计 API ====================

@router.get("/stats/count", tags=["Contracts"])
async def count_contracts(
    db: AsyncSession = Depends(get_db),
    student_id: Optional[int] = Query(None, description="学员ID筛选"),
    course_id: Optional[int] = Query(None, description="课程ID筛选"),
    status: Optional[int] = Query(None, ge=1, le=4, description="状态筛选"),
):
    """统计合同数量"""
    try:
        count = await ContractService.count_contracts(
            session=db,
            student_id=student_id,
            course_id=course_id,
            status=status
        )
        return {"count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"统计合同数量失败: {str(e)}"
        )

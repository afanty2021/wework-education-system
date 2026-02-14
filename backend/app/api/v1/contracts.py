"""Contracts API Routes

合同管理相关 API 路由
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.contract import ContractCreate, ContractResponse, ContractUpdate

router = APIRouter()


@router.get("", response_model=List[ContractResponse], tags=["Contracts"])
async def list_contracts(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[ContractResponse]:
    """获取合同列表"""
    # TODO: 实现合同列表查询
    pass


@router.get("/{contract_id}", response_model=ContractResponse, tags=["Contracts"])
async def get_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """获取合同详情"""
    # TODO: 实现合同详情查询
    pass


@router.post("", response_model=ContractResponse, status_code=status.HTTP_201_CREATED, tags=["Contracts"])
async def create_contract(
    contract_data: ContractCreate,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """创建合同"""
    # TODO: 实现合同创建
    pass


@router.put("/{contract_id}", response_model=ContractResponse, tags=["Contracts"])
async def update_contract(
    contract_id: int,
    contract_data: ContractUpdate,
    db: AsyncSession = Depends(get_db),
) -> ContractResponse:
    """更新合同"""
    # TODO: 实现合同更新
    pass


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Contracts"])
async def delete_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除合同"""
    # TODO: 实现合同删除
    pass

from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
async def connection():
    #TODO
    pass

@router.post("/login")
async def connecte():
    #TODO
    pass

@router.get("/sign_in")
async def inscription():
    #TODO
    pass

@router.post("/sign_in")
async def creationCompte():
    #TODO
    pass
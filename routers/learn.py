from fastapi import Request, APIRouter
from utils.model import train_evaluate_update
from response.response import CustomResponse






router = APIRouter(tags=["Learn"], prefix="/learn")





@router.post("/train-data")
async def train(request:Request):

    loss, accuracy = await train_evaluate_update(3, "static/model_data")

    print(loss)

    print(accuracy)

    data = {"accuracy": accuracy, "loss": loss}

    return CustomResponse("Model Trained Successfully", data=data)
from fastapi import FastAPI, APIRouter
from src.api.api_v1.api import api_router
from src.configs.settings import get_settings

# Runtime Settings/Environment Configuration
settings = get_settings()

description = """
This project is part of [Data Science 4 All - DS4A](https://www.correlation-one.com/data-science-for-all-colombia) \
training 🚀, and has two main objectives:

<ul style="list-style-type:disc;">
    <li>
        Building a classification model that will give a prediction about the probability of a student dropouts the school.<br>
        The model will be treated as a <strong>binary classification problem</strong>. So, 0 will be the class who does not
        dropout the school and 1 will be the class who dropouts the school.
    </li>
    <li>
        Build an interactive <strong>dashboard</strong> for <a href="https://www.sogamoso-boyaca.gov.co/" target="blank">Sogamoso municipality</a> 
        to interpret the predictions made by the model, and improve the  knowledge to allows the making-decision.
    </li>
</ul>
"""

app = FastAPI(
    title="School dropout Sogamoso - Backend",
    description=description,
    version=settings.FAST_API_VERSION,
    openapi_url="/openapi.json",
    contact={
        "name": "Samir Hinojosa",
        "url": "https://www.samirhinojosa.com/",
        "email": "samirhinojosa@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)


app.include_router(api_router, prefix=settings.API_VERSION)
api_router = APIRouter()
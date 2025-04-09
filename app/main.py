from fastapi import FastAPI
from app.api import user, auth, sports_complex, court, court_availability, booking_slot, public_view

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(sports_complex.router)
app.include_router(court.router)
app.include_router(court_availability.router)
app.include_router(booking_slot.router)
app.include_router(public_view.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to your sports booking app!"}

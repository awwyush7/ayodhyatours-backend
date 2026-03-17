from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from datetime import datetime
import os
from typing import Optional

# Initialize FastAPI app
app = FastAPI(title="Ayodhya Tours API", version="1.0.0")

# CORS middleware - allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Configuration
SUPABASE_URL = "https://bshqllemdktagcbwqohl.supabase.co"
SUPABASE_KEY = "sb_publishable_gag22Ya5fTvMHt1kbLrxkg_Q2Fin77M"  # Use service_role key for backend

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Pydantic Models for request validation
class ContactInquiry(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    message: Optional[str] = None


class Booking(BaseModel):
    customer_name: str
    email: EmailStr
    phone: str
    package_name: str
    number_of_people: int
    preferred_date: Optional[str] = None


# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": "Ayodhya Tours API is running!",
        "status": "active",
        "version": "1.0.0"
    }


# Contact Form Submission
@app.post("/api/contact")
async def submit_contact_form(inquiry: ContactInquiry):
    """
    Submit a contact inquiry to the database
    """
    try:
        # Insert into Supabase
        data = {
            "full_name": inquiry.full_name,
            "email": inquiry.email,
            "phone": inquiry.phone,
            "message": inquiry.message,
            "created_at": datetime.utcnow().isoformat()
        }
        
        response = supabase.table("contact_inquiries").insert(data).execute()
        
        # TODO: Send email notification here using SendGrid/Resend
        # send_email_notification(inquiry)
        
        return {
            "success": True,
            "message": "Thank you for your inquiry! We'll get back to you soon.",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting inquiry: {str(e)}")


# Get all contact inquiries (Admin only)
@app.get("/api/contact")
async def get_contact_inquiries():
    """
    Retrieve all contact inquiries
    """
    try:
        response = supabase.table("contact_inquiries").select("*").order("created_at", desc=True).execute()
        return {
            "success": True,
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching inquiries: {str(e)}")


# Create a booking
@app.post("/api/bookings")
async def create_booking(booking: Booking):
    """
    Create a new tour booking
    """
    try:
        data = {
            "customer_name": booking.customer_name,
            "email": booking.email,
            "phone": booking.phone,
            "package_name": booking.package_name,
            "number_of_people": booking.number_of_people,
            "preferred_date": booking.preferred_date,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        response = supabase.table("bookings").insert(data).execute()
        
        # TODO: Send confirmation email and SMS
        # send_booking_confirmation(booking)
        
        return {
            "success": True,
            "message": "Booking created successfully! We'll contact you soon.",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating booking: {str(e)}")


# Get all bookings (Admin only)
@app.get("/api/bookings")
async def get_bookings():
    """
    Retrieve all bookings
    """
    try:
        response = supabase.table("bookings").select("*").order("created_at", desc=True).execute()
        return {
            "success": True,
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bookings: {str(e)}")


# Update booking status (Admin only)
@app.patch("/api/bookings/{booking_id}")
async def update_booking_status(booking_id: str, status: str):
    """
    Update booking status (pending, confirmed, completed, cancelled)
    """
    try:
        response = supabase.table("bookings").update({"status": status}).eq("id", booking_id).execute()
        return {
            "success": True,
            "message": f"Booking status updated to {status}",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating booking: {str(e)}")


# Get tour packages
@app.get("/api/packages")
async def get_tour_packages():
    """
    Retrieve all tour packages
    """
    try:
        response = supabase.table("tour_packages").select("*").execute()
        return {
            "success": True,
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching packages: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

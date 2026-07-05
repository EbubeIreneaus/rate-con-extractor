from pydantic import BaseModel, Field

class Load(BaseModel):
    load_number: str = Field(description="the broker's internal load/reference ID (e.g. \"NP-88214\", \"HRL-4471\")")
    broker_name: str = Field(description="The name of the broker")
    broker_mc_number: str = Field(description="A unique authority operating identifier issue by FMCSA")
    carrier_name: str = Field(description="The name of the carrier")
    carrier_mc_number: str = Field(description="A unique authority operating identifier issue by FMCSA")
    equipment_type: str = Field(description="The type of equipment required for the load (e.g. \"Van\", \"Flatbed\", \"Reefer\")")
    weight: str = Field(description="The weight of the load in pounds (e.g. \"10,000 lbs\", \"20,000 lbs\")")
    commodity: str = Field(description="The type of goods being transported (e.g. \"Electronics\", \"Furniture\", \"Food Products\")")


class Pickup(BaseModel):
    pickup_date: str = Field(description="The date the load is to be picked up")
    pickup_time: str = Field(description="The time the load is to be picked up")
    pickup_location_name: str | None = Field(default=None, description="shipper/facility name (optional — not every doc names one)")
    pickup_city: str = Field(description="The city where the load is to be picked up")
    pickup_state: str = Field(description="The state where the load is to be picked up")
    pickup_zip: str = Field(description="The zip code where the load is to be picked up")
    pickup_address: str | None = Field(default=None, description="The address where the load is to be picked up optional")

class Delivery(BaseModel):
    delivery_date: str = Field(description="The date the load is to be delivered")
    delivery_time: str = Field(description="The time the load is to be delivered")
    delivery_location_name: str | None = Field(default=None, description="consignee/facility name (optional — not every doc names one)")
    delivery_city: str = Field(description="The city where the load is to be delivered")
    delivery_state: str = Field(description="The state where the load is to be delivered")
    delivery_zip: str = Field(description="The zip code where the load is to be delivered")
    delivery_address: str | None = Field(default=None, description="The address where the load is to be delivered optional")

class RateItem(BaseModel):
    description: str = Field(description="The rate item (e.g. \"Base Rate\", \"Fuel Surcharge\")")
    amount: float = Field(description="The amount for the rate item e.g $200.00, $300.00")

class Rate(BaseModel):
    total_rate: float = Field(description="The total rate for the load (e.g. 1500.00, 2000.00)")
    rate_breakdown: list[RateItem] | None = Field(default=None, description="A breakdown of the rate, if available (optional — not every doc provides this information)")
    payment_terms: str | None = Field(default=None, description="The payment terms for the load (e.g. \"Net 30\", \"COD\") (optional — not every doc provides this information)")

class RateConfirmation(BaseModel):
    load: Load = Field(description="The load information")
    pickup: Pickup = Field(description="The pickup information")
    delivery: Delivery = Field(description="The delivery information")
    rate: Rate = Field(description="The rate information")

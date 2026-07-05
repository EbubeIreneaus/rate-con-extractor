# Rate Confirmation Extractor

## Problem
Freight brokers and forwarders spend valuable time manually reviewing Rate Confirmation PDFs and typing shipment details into their TMS or internal systems. This process is slow, repetitive, and prone to human error, especially when each carrier sends documents in different layouts and formats.

Every rate confirmation contains critical shipment information such as:
- Load details
- Pickup information
- Delivery information
- Rate and charge details

Manually extracting this data creates bottlenecks, slows down operations, and takes staff away from higher-value work such as customer calls, follow-ups, and deal-making.

## Solution
This project demonstrates an AI-powered automation workflow that reads a Rate Confirmation PDF, extracts the relevant fields, and presents the information in a structured format for review.

Although this demo currently displays the extracted information to the user, the same workflow can be connected to a TMS through an API. In that setup, the extracted data can be pushed directly into the operating system used by the brokerage or forwarder, removing the need for manual typing and reducing administrative overhead.

## What This Demo Shows
- Upload a Rate Confirmation PDF
- Extract key shipment and rate information automatically
- View structured output in a clean, user-friendly interface
- Demonstrate how the same automation can be integrated with a TMS later

## Why This Matters for Freight Brokers and Forwarders
For freight brokers and forwarders, time is money. Automation helps teams:
- Reduce manual data entry
- Improve accuracy and consistency
- Speed up booking and dispatch workflows
- Free up staff to focus on calls, relationships, and revenue-generating activity

Instead of spending time copying data from documents into systems, teams can focus on moving freight and growing business.

## Validation
The solution was tested with three sample Rate Confirmation PDFs in different formats. In all three cases, the relevant data was extracted successfully with 100% accuracy in the tested scenarios.

## Ideal Use Case
This solution is especially valuable for businesses that receive rate confirmations from multiple carriers and need a faster, more reliable way to turn documents into structured operational data.

## Future Direction
This demo is designed to show the core value of the automation. In a production setup, the extracted data can be sent to a client-specific TMS or workflow system through API integration, making the process fully automated from document intake to system entry.

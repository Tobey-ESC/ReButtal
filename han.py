import streamlit as st
from streamlit.components.v1 import html
import time
import pyperclip
from datetime import datetime

def load_templates():
    templates = {
        "PAID BY OTHER MEANS": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER PAID BY OTHER MEANS. OUR CARDHOLDER CONFIRMS THAT THEY USED [ALTERNATE_PAYMENT] ON [PAYMENT_DATE] TO PAY FOR [PRODUCT]. ACCORDING TO VISA REGULATIONS, MERCHANTS MUST ENSURE THEY HAVE PROPER AUTHORIZATION FOR ANY CHARGES. OUR CARDHOLDER ATTEMPTED TO CONTACT THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT DID NOT RECEIVE A RESOLUTION. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE WITH THE MERCHANT HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER PAID BY OTHER MEANS. OUR CARDHOLDER INDICATES THAT PAYMENT WAS MADE USING [ALTERNATE_PAYMENT] ON [PAYMENT_DATE], RENDERING THIS TRANSACTION INVALID. MASTERCARD GUIDELINES REQUIRE MERCHANTS TO CONFIRM AUTHORIZATION PRIOR TO CHARGING A CARDHOLDER. OUR CARDHOLDER REACHED OUT TO THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT RECEIVED NO ASSISTANCE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "NON-RECEIPT OF MERCHANDISE/SERVICE": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER NON-RECEIPT OF MERCHANDISE/SERVICE. OUR CARDHOLDER ORDERED [PRODUCT] ON [ORDER_DATE], EXPECTING DELIVERY BY [EXPECTED_DELIVERY_DATE], BUT NO MERCHANDISE HAS BEEN RECEIVED. ACCORDING TO VISA REGULATIONS, MERCHANTS MUST FULFILL ORDERS IN A TIMELY MANNER. OUR CARDHOLDER ATTEMPTED TO CONTACT THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT RECEIVED NO RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER NON-RECEIPT OF MERCHANDISE/SERVICE. OUR CARDHOLDER PLACED AN ORDER FOR [PRODUCT] ON [ORDER_DATE] BUT HAS NOT RECEIVED IT AS OF TODAY. MASTERCARD REGULATIONS REQUIRE MERCHANTS TO DELIVER PRODUCTS PROMPTLY OR NOTIFY CARDHOLDERS OF ANY DELAYS. OUR CARDHOLDER CONTACTED THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] FOR AN UPDATE BUT RECEIVED NO ASSISTANCE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "INCORRECT AMOUNT": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR AN INCORRECT AMOUNT OF [AMOUNT] BILLED ON [DATE]. OUR CARDHOLDER AUTHORIZED A PAYMENT OF [EXPECTED_AMOUNT] FOR [PRODUCT], BUT WAS CHARGED [DISPUTED_AMOUNT]. ACCORDING TO VISA GUIDELINES, MERCHANTS MUST CHARGE THE AUTHORIZED AMOUNT. OUR CARDHOLDER ATTEMPTED TO CONTACT THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] TO REQUEST A CORRECTION, BUT NO ACTION WAS TAKEN. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR AN INCORRECT AMOUNT OF [AMOUNT] BILLED ON [DATE]. OUR CARDHOLDER AUTHORIZED A PAYMENT OF [EXPECTED_AMOUNT] FOR [PRODUCT] BUT WAS INCORRECTLY CHARGED [DISPUTED_AMOUNT]. MASTERCARD REGULATIONS MANDATE THAT MERCHANTS MUST ENSURE THE FINAL BILLING AMOUNT MATCHES THE AUTHORIZED AMOUNT. OUR CARDHOLDER ATTEMPTED TO RESOLVE THIS WITH THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT DID NOT RECEIVE ASSISTANCE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "DUPLICATE BILLING": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A DUPLICATE CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE]. OUR CARDHOLDER MADE A PAYMENT OF [AMOUNT] FOR [PRODUCT] ON [INITIAL_TRANSACTION_DATE] BUT WAS CHARGED AGAIN ON [DUPLICATE_TRANSACTION_DATE]. VISA REGULATIONS STATE THAT MERCHANTS MUST ENSURE THAT DUPLICATE BILLING IS AVOIDED UNLESS CLEAR AUTHORIZATION EXISTS. OUR CARDHOLDER CONTACTED THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] FOR ASSISTANCE BUT DID NOT RECEIVE A RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A DUPLICATE CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE]. OUR CARDHOLDER AUTHORIZED A PAYMENT FOR [PRODUCT] ON [INITIAL_TRANSACTION_DATE] BUT WAS INCORRECTLY BILLED AGAIN ON [DUPLICATE_TRANSACTION_DATE]. MASTERCARD GUIDELINES REQUIRE MERCHANTS TO ENSURE THAT DUPLICATE CHARGES DO NOT OCCUR WITHOUT CLEAR AUTHORIZATION. OUR CARDHOLDER TRIED TO CONTACT THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] TO RESOLVE THIS ISSUE BUT RECEIVED NO RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "NOT AS DESCRIBED MERCHANDISE/SERVICE": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER NOT AS DESCRIBED MERCHANDISE/SERVICE. OUR CARDHOLDER PURCHASED [PRODUCT] ON [ORDER_DATE], BUT IT DID NOT MATCH THE DESCRIPTION. VISA REGULATIONS REQUIRE THAT ALL PRODUCTS AND SERVICES MUST BE AS DESCRIBED AT THE TIME OF SALE. OUR CARDHOLDER ATTEMPTED TO RESOLVE THIS WITH THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT DID NOT RECEIVE A RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER NOT AS DESCRIBED MERCHANDISE/SERVICE. OUR CARDHOLDER ORDERED [PRODUCT] ON [ORDER_DATE], BUT IT DID NOT MEET THE EXPECTATIONS SET FORTH BY THE MERCHANT. MASTERCARD REGULATIONS STATE THAT MERCHANTS MUST DELIVER PRODUCTS THAT MATCH THEIR DESCRIPTIONS. OUR CARDHOLDER TRIED TO CONTACT THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT RECEIVED NO ASSISTANCE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "DAMAGED OR DEFECTIVE MERCHANDISE/SERVICE": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER DAMAGED OR DEFECTIVE MERCHANDISE/SERVICE. OUR CARDHOLDER RECEIVED [PRODUCT] ON [RECEIPT_DATE], BUT IT WAS DAMAGED/DEFECTIVE. VISA GUIDELINES REQUIRE MERCHANTS TO ENSURE THAT ALL PRODUCTS DELIVERED TO CARDHOLDERS ARE IN GOOD CONDITION. OUR CARDHOLDER ATTEMPTED TO RETURN THE DAMAGED ITEM ON [CONTACT_DATE] AT [PHONE_NUMBER], BUT DID NOT RECEIVE ASSISTANCE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER DAMAGED OR DEFECTIVE MERCHANDISE/SERVICE. OUR CARDHOLDER RECEIVED [PRODUCT] ON [RECEIPT_DATE], BUT IT WAS DAMAGED/DEFECTIVE UPON ARRIVAL. MASTERCARD REGULATIONS STATE THAT MERCHANTS MUST PROVIDE PRODUCTS THAT ARE IN A SATISFACTORY CONDITION. OUR CARDHOLDER TRIED TO RETURN THE ITEM ON [CONTACT_DATE] AT [PHONE_NUMBER], BUT NO ASSISTANCE WAS OFFERED. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "ADDENDUM": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER ADDENDUM. THE ORIGINAL TRANSACTION WAS FOR [PRODUCT], BUT DUE TO [REFERENCE_NUMBER], OUR CARDHOLDER BELIEVES A REFUND IS WARRANTED. ACCORDING TO VISA REGULATIONS, MERCHANTS MUST PROVIDE CLARITY AND ADDRESS DISPUTES THOROUGHLY. OUR CARDHOLDER ATTEMPTED TO RESOLVE THIS WITH THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER], BUT RECEIVED NO ASSISTANCE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER ADDENDUM. THE ORIGINAL TRANSACTION WAS FOR [PRODUCT], BUT DUE TO [REFERENCE_NUMBER], OUR CARDHOLDER SEEKS A REFUND. MASTERCARD REGULATIONS REQUIRE MERCHANTS TO ENSURE THAT ALL DISPUTES ARE HANDLED APPROPRIATELY. OUR CARDHOLDER ATTEMPTED TO CONTACT THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER], BUT DID NOT RECEIVE A RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "CANCELLED MERCHANDISE/SERVICE": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] FOR CANCELLED MERCHANDISE/SERVICE. OUR CARDHOLDER CANCELLED THE ORDER FOR [PRODUCT] ON [CANCELLATION_DATE] AND WAS EXPECTED TO RECEIVE A FULL REFUND. VISA REGULATIONS REQUIRE MERCHANTS TO ISSUE CREDITS PROMPTLY FOR CANCELLED SERVICES. OUR CARDHOLDER CONTACTED THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT DID NOT RECEIVE A REFUND. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] FOR CANCELLED MERCHANDISE/SERVICE. OUR CARDHOLDER CANCELLED THE ORDER FOR [PRODUCT] ON [CANCELLATION_DATE] BUT HAS NOT RECEIVED A REFUND. MASTERCARD GUIDELINES STATE THAT MERCHANTS MUST REFUND CARDHOLDERS PROMPTLY UPON CANCELLATION. OUR CARDHOLDER ATTEMPTED TO CONTACT THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT RECEIVED NO ASSISTANCE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "CANCELLED RECURRING TRANSACTION": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER CANCELLED RECURRING TRANSACTION. OUR CARDHOLDER CANCELLED THE RECURRING PAYMENT ON [CANCELLATION_DATE] BUT WAS STILL BILLED. VISA REGULATIONS REQUIRE MERCHANTS TO HALT BILLING IMMEDIATELY UPON CANCELLATION. OUR CARDHOLDER CONTACTED THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] FOR RESOLUTION BUT DID NOT RECEIVE A REFUND. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] FOR CANCELLED RECURRING TRANSACTION. OUR CARDHOLDER INITIATED CANCELLATION OF THE RECURRING CHARGE ON [CANCELLATION_DATE], YET WAS STILL BILLED. MASTERCARD GUIDELINES REQUIRE MERCHANTS TO IMMEDIATELY CEASE BILLING FOLLOWING CANCELLATION REQUESTS. OUR CARDHOLDER REACHED OUT TO THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT DID NOT GET A RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "CUSTOMER NOT PROPERLY NOTIFIED": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER CUSTOMER NOT PROPERLY NOTIFIED. OUR CARDHOLDER DID NOT RECEIVE PROPER NOTIFICATION OF [PRODUCT] AS REQUIRED. VISA REGULATIONS MANDATE THAT MERCHANTS PROVIDE CLEAR NOTICE TO CARDHOLDERS BEFORE CHARGES ARE BILLED. OUR CARDHOLDER ATTEMPTED TO CONTACT THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] FOR CLARIFICATION BUT RECEIVED NO ASSISTANCE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] UNDER CUSTOMER NOT PROPERLY NOTIFIED. OUR CARDHOLDER WAS NOT NOTIFIED OF [PRODUCT] AS REQUIRED BY MASTERCARD REGULATIONS. MERCHANTS MUST ENSURE THAT CARDHOLDERS ARE PROPERLY INFORMED BEFORE PROCESSING CHARGES. OUR CARDHOLDER ATTEMPTED TO RESOLVE THIS WITH THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT RECEIVED NO RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "CREDIT NOT PROCESSED WITH CREDIT SLIP": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] DUE TO A CREDIT NOT PROCESSED WITH CREDIT SLIP. OUR CARDHOLDER RETURNED [PRODUCT] AND WAS PROMISED A CREDIT ON [CREDIT_DATE] BUT HAS NOT RECEIVED IT. ACCORDING TO VISA REGULATIONS, MERCHANTS MUST PROCESS CREDITS PROMPTLY ONCE A CREDIT SLIP HAS BEEN PROVIDED. OUR CARDHOLDER ATTEMPTED TO CONTACT THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT DID NOT GET A RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] BECAUSE A CREDIT WAS NOT PROCESSED WITH THE CREDIT SLIP. AFTER RETURNING [PRODUCT] ON [RETURN_DATE], OUR CARDHOLDER WAS ASSURED A CREDIT WOULD BE ISSUED BUT HAS NOT RECEIVED IT. MASTERCARD REGULATIONS REQUIRE MERCHANTS TO PROCESS REFUNDS PROMPTLY. OUR CARDHOLDER CONTACTED THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT DID NOT RECEIVE ASSISTANCE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        },
        "CREDIT NOT PROCESSED FOR CANCELLED MERCHANDISE/ORDER/SERVICE": {
            "Visa": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] BECAUSE A CREDIT WAS NOT PROCESSED FOR CANCELLED MERCHANDISE/ORDER/SERVICE. AFTER CANCELING THE ORDER ON [CANCELLATION_DATE], OUR CARDHOLDER HAS NOT RECEIVED A CREDIT AS PROMISED. VISA REGULATIONS REQUIRE MERCHANTS TO ISSUE REFUNDS PROMPTLY UPON CANCELLATION. OUR CARDHOLDER ATTEMPTED TO REACH THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] FOR A RESOLUTION BUT RECEIVED NO RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT.""",
            "Mastercard": """OUR CARDHOLDER IS DISPUTING A CHARGE FROM [MERCHANT] FOR [AMOUNT] BILLED ON [DATE] BECAUSE A CREDIT WAS NOT PROCESSED FOR CANCELLED MERCHANDISE/ORDER/SERVICE. OUR CARDHOLDER CANCELLED THE ORDER ON [CANCELLATION_DATE] AND EXPECTED A REFUND, BUT IT HAS NOT BEEN PROCESSED. MASTERCARD GUIDELINES REQUIRE MERCHANTS TO ISSUE CREDITS IMMEDIATELY AFTER CANCELLATION. OUR CARDHOLDER CONTACTED THE MERCHANT ON [CONTACT_DATE] AT [PHONE_NUMBER] BUT DID NOT RECEIVE A RESPONSE. ALL REASONABLE ATTEMPTS TO RESOLVE THIS ISSUE HAVE BEEN UNSUCCESSFUL, AND OUR CARDHOLDER IS DUE THE REQUESTED CREDIT."""
        }
    }
    return templates

def validate_number(value, field_name):
    """Validate if input contains only numbers"""
    if value and not value.replace('.', '').replace('$', '').replace(',', '').isdigit():
        error_gif = """
            <div style="display: flex; justify-content: flex-start; align-items: center;">
                <iframe src="https://giphy.com/embed/fxeWwyOg76A9sDP06s" 
                        width="100" 
                        height="75" 
                        frameBorder="0" 
                        class="giphy-embed">
                </iframe>
            </div>
        """.format(field_name)
        st.markdown(error_gif, unsafe_allow_html=True)
        return False
    return True

def validate_text(value, field_name):
    """Validate if input contains only text"""
    if value and any(char.isdigit() for char in value):
        error_gif = """
            <div style="display: flex; justify-content: flex-start; align-items: center;">
                <iframe src="https://giphy.com/embed/fxeWwyOg76A9sDP06s" 
                        width="100" 
                        height="75" 
                        frameBorder="0" 
                        class="giphy-embed">
                </iframe>
                
            </div>
        """.format(field_name)
        st.markdown(error_gif, unsafe_allow_html=True)
        return False
    return True

def validate_alphanumeric(value, field_name):
    """Validate if input contains alphanumeric characters"""
    # This function doesn't need to validate anything since we accept both letters and numbers
    return True

def create_pulsating_circle_css():
    return """
    <style>
        .circle-container {
            position: fixed;
            bottom: 20px;
            left: 20px;
            display: flex;
            gap: 10px;
        }
        .circle {
            width: 12px;
            height: 12px;
            background-color: #00ff00;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 10px rgba(0, 255, 0, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(0, 255, 0, 0);
            }
        }
    </style>
    """

def generate_rebuttal():
    templates = load_templates()
    
    # Get the current template based on selected reason code and card type
    template = templates[st.session_state.reason_code][st.session_state.card_type]
    
    # Replace placeholders with existing values
    if hasattr(st.session_state, 'merchant'):
        template = template.replace('[MERCHANT]', st.session_state.merchant)
    if hasattr(st.session_state, 'amount'):
        template = template.replace('[AMOUNT]', st.session_state.amount)
    if hasattr(st.session_state, 'transaction_date'):
        template = template.replace('[DATE]', st.session_state.transaction_date.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'contact_date'):
        template = template.replace('[CONTACT_DATE]', st.session_state.contact_date.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'phone_number'):
        template = template.replace('[PHONE_NUMBER]', st.session_state.phone_number)
    if hasattr(st.session_state, 'product'):
        template = template.replace('[PRODUCT]', st.session_state.product)
    if hasattr(st.session_state, 'reference_number_main'):
        template = template.replace('[REFERENCE_NUMBER]', st.session_state.reference_number_main)
    if hasattr(st.session_state, 'alternate_payment'):
        template = template.replace('[ALTERNATE_PAYMENT]', st.session_state.alternate_payment)
    if hasattr(st.session_state, 'payment_date'):
        template = template.replace('[PAYMENT_DATE]', st.session_state.payment_date.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'order_date'):
        template = template.replace('[ORDER_DATE]', st.session_state.order_date.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'expected_delivery'):
        template = template.replace('[EXPECTED_DELIVERY_DATE]', st.session_state.expected_delivery.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'expected_amount'):
        template = template.replace('[EXPECTED_AMOUNT]', st.session_state.expected_amount)
    if hasattr(st.session_state, 'initial_transaction'):
        template = template.replace('[INITIAL_TRANSACTION_DATE]', st.session_state.initial_transaction.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'duplicate_transaction'):
        template = template.replace('[DUPLICATE_TRANSACTION_DATE]', st.session_state.duplicate_transaction.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'receipt_date'):
        template = template.replace('[RECEIPT_DATE]', st.session_state.receipt_date.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'cancellation_date'):
        template = template.replace('[CANCELLATION_DATE]', st.session_state.cancellation_date.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'credit_date'):
        template = template.replace('[CREDIT_DATE]', st.session_state.credit_date.strftime("%m/%d/%Y"))
    if hasattr(st.session_state, 'return_date'):
        template = template.replace('[RETURN_DATE]', st.session_state.return_date.strftime("%m/%d/%Y"))
    
    # Update the current template
    st.session_state.current_template = template

def main():
    # Custom CSS for the title
    st.markdown("""
        <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            color: #2e2e2e;
            text-align: center;
            margin-bottom: 30px;
            font-family: 'Helvetica Neue', sans-serif;
            text-transform: none;
            letter-spacing: 1px;
        }
        .title span {
            color: #ff4b4b;
        }
        </style>
        <div class="title">
            Re <span>Butt(al)</span>
        </div>
    """, unsafe_allow_html=True)

    # Add the CSS to the page
    st.markdown(create_pulsating_circle_css(), unsafe_allow_html=True)
    
    # Initialize all session state variables
    if 'generated' not in st.session_state:
        st.session_state.generated = False
    if 'input_values' not in st.session_state:
        st.session_state.input_values = {}
    if 'current_template' not in st.session_state:
        st.session_state.current_template = ""
    if 'previous_card_type' not in st.session_state:
        st.session_state.previous_card_type = None
    if 'previous_reason_code' not in st.session_state:
        st.session_state.previous_reason_code = None
    if 'active_users' not in st.session_state:
        st.session_state.active_users = 1  # Initialize with 1 active user

    templates = load_templates()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        reason_code = st.selectbox(
            "Select Reason Code",
            options=[
                "PAID BY OTHER MEANS",
                "NON-RECEIPT OF MERCHANDISE/SERVICE",
                "INCORRECT AMOUNT",
                "DUPLICATE BILLING",
                "NOT AS DESCRIBED MERCHANDISE/SERVICE",
                "DAMAGED OR DEFECTIVE MERCHANDISE/SERVICE",
                "ADDENDUM",
                "CANCELLED MERCHANDISE/SERVICE",
                "CANCELLED RECURRING TRANSACTION",
                "CUSTOMER NOT PROPERLY NOTIFIED",
                "CREDIT NOT PROCESSED WITH CREDIT SLIP",
                "CREDIT NOT PROCESSED FOR CANCELLED MERCHANDISE/ORDER/SERVICE"
            ],
            key='reason_code'
        )
        
        card_type = st.radio(
            "Select Card Type",
            ["Visa", "Mastercard"],
            key='card_type'
        )

        # Check if card type or reason code has changed
        if (st.session_state.previous_card_type != card_type or 
            st.session_state.previous_reason_code != reason_code) and st.session_state.generated:
            
            # Get the new template
            template = templates[reason_code][card_type]
            
            # Replace placeholders with existing values
            if hasattr(st.session_state, 'merchant'):
                template = template.replace('[MERCHANT]', st.session_state.merchant)
            if hasattr(st.session_state, 'amount'):
                template = template.replace('[AMOUNT]', st.session_state.amount)
            if hasattr(st.session_state, 'transaction_date'):
                template = template.replace('[DATE]', st.session_state.transaction_date.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'contact_date'):
                template = template.replace('[CONTACT_DATE]', st.session_state.contact_date.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'phone_number'):
                template = template.replace('[PHONE_NUMBER]', st.session_state.phone_number)
            if hasattr(st.session_state, 'product'):
                template = template.replace('[PRODUCT]', st.session_state.product)
            if hasattr(st.session_state, 'reference_number_main'):
                template = template.replace('[REFERENCE_NUMBER]', st.session_state.reference_number_main)
            if hasattr(st.session_state, 'alternate_payment'):
                template = template.replace('[ALTERNATE_PAYMENT]', st.session_state.alternate_payment)
            if hasattr(st.session_state, 'payment_date'):
                template = template.replace('[PAYMENT_DATE]', st.session_state.payment_date.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'order_date'):
                template = template.replace('[ORDER_DATE]', st.session_state.order_date.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'expected_delivery'):
                template = template.replace('[EXPECTED_DELIVERY_DATE]', st.session_state.expected_delivery.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'expected_amount'):
                template = template.replace('[EXPECTED_AMOUNT]', st.session_state.expected_amount)
            if hasattr(st.session_state, 'initial_transaction'):
                template = template.replace('[INITIAL_TRANSACTION_DATE]', st.session_state.initial_transaction.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'duplicate_transaction'):
                template = template.replace('[DUPLICATE_TRANSACTION_DATE]', st.session_state.duplicate_transaction.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'receipt_date'):
                template = template.replace('[RECEIPT_DATE]', st.session_state.receipt_date.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'cancellation_date'):
                template = template.replace('[CANCELLATION_DATE]', st.session_state.cancellation_date.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'credit_date'):
                template = template.replace('[CREDIT_DATE]', st.session_state.credit_date.strftime("%m/%d/%Y"))
            if hasattr(st.session_state, 'return_date'):
                template = template.replace('[RETURN_DATE]', st.session_state.return_date.strftime("%m/%d/%Y"))
            
            # Update the current template
            st.session_state.current_template = template
            
        # Update the previous values
        st.session_state.previous_card_type = card_type
        st.session_state.previous_reason_code = reason_code
        
        # Merchant name - text only
        merchant = st.text_input("Merchant Name", key='merchant')
        if merchant:
            validate_text(merchant, "Merchant Name")
        
        # Amount - numbers only
        amount = st.text_input("Disputed Amount", key='amount')
        if amount:
            validate_number(amount, "Amount")
        
        transaction_date = st.date_input("Transaction Date", key='transaction_date')
    
    # Additional Information (Column 2)
    with col2:
        contact_date = st.date_input("Contact Date", key='contact_date')
        
        # Phone number - numbers only
        phone_number = st.text_input("Phone Number", key='phone_number')
        if phone_number:
            validate_number(phone_number, "Phone Number")
        
        # Reference number - alphanumeric allowed
        reference_number = st.text_input("Reference Number", key='reference_number_main')
        if reference_number:
            validate_alphanumeric(reference_number, "Reference Number")
        
        # Valid amount - numbers only
        valid_amount = st.text_input("Valid Amount", key='valid_amount')
        if valid_amount:
            validate_number(valid_amount, "Valid Amount")
        
        valid_transaction = st.date_input("Valid Transaction Date", key='valid_transaction')
    
    # Reason-specific fields (Column 3)
    with col3:
        if reason_code == "PAID BY OTHER MEANS":
            # Product/Service Description - text only
            product = st.text_input("Product/Service Description", key='product')
            if product:
                validate_text(product, "Product/Service Description")
                
            alternate_payment = st.text_input("Alternate Payment Method", key='alternate_payment')
            if alternate_payment:
                validate_text(alternate_payment, "Alternate Payment Method")
            payment_date = st.date_input("Payment Date", key='payment_date')
            
        elif reason_code == "NON-RECEIPT OF MERCHANDISE/SERVICE":
            product = st.text_input("Product/Service Description", key='product')
            if product:
                validate_text(product, "Product/Service Description")
            order_date = st.date_input("Order Date", key='order_date')
            expected_delivery = st.date_input("Expected Delivery Date", key='expected_delivery')
            
        elif reason_code == "INCORRECT AMOUNT":
            product = st.text_input("Product/Service Description", key='product')
            if product:
                validate_text(product, "Product/Service Description")
            expected_amount = st.text_input("Expected Amount", key='expected_amount')
            if expected_amount:
                validate_number(expected_amount, "Expected Amount")
            
        elif reason_code == "DUPLICATE BILLING":
            product = st.text_input("Product/Service Description", key='product')
            initial_transaction = st.date_input("Initial Transaction Date", key='initial_transaction')
            duplicate_transaction = st.date_input("Duplicate Transaction Date", key='duplicate_transaction')
            
        elif reason_code == "NOT AS DESCRIBED MERCHANDISE/SERVICE":
            product = st.text_input("Product/Service Description", key='product')
            order_date = st.date_input("Order Date", key='order_date')
            
        elif reason_code == "DAMAGED OR DEFECTIVE MERCHANDISE/SERVICE":
            product = st.text_input("Product/Service Description", key='product')
            receipt_date = st.date_input("Receipt Date", key='receipt_date')
            
        elif reason_code == "CANCELLED MERCHANDISE/SERVICE":
            product = st.text_input("Product/Service Description", key='product')
            cancellation_date = st.date_input("Cancellation Date", key='cancellation_date')
            
        elif reason_code == "CANCELLED RECURRING TRANSACTION":
            product = st.text_input("Product/Service Description", key='product')
            cancellation_date = st.date_input("Cancellation Date", key='cancellation_date')
            
        elif reason_code == "CREDIT NOT PROCESSED WITH CREDIT SLIP":
            product = st.text_input("Product/Service Description", key='product')
            credit_date = st.date_input("Credit Date", key='credit_date')
            return_date = st.date_input("Return Date", key='return_date')
            
        elif reason_code == "CREDIT NOT PROCESSED FOR CANCELLED MERCHANDISE/ORDER/SERVICE":
            product = st.text_input("Product/Service Description", key='product')
            cancellation_date = st.date_input("Cancellation Date", key='cancellation_date')
            
        elif reason_code == "ADDENDUM":
            product = st.text_input("Product/Service Description", key='product')
            if product:
                validate_text(product, "Product/Service Description")
            reference_number_addendum = st.text_input("Reference Number for Addendum", key='reference_number_addendum')
            if reference_number_addendum:
                validate_text(reference_number_addendum, "Reference Number")
            
        elif reason_code == "CUSTOMER NOT PROPERLY NOTIFIED":
            product = st.text_input("Product/Service Description", key='product')
            
    # Create two columns for the buttons
    button_col1, button_col2 = st.columns([1, 1])
    
    with button_col1:
        if st.button("Generate Rebuttal", key="generate_button"):
            st.session_state.generated = True
            generate_rebuttal()
    
    # Display the rebuttal if generated (read-only)
    if st.session_state.generated:
        # First display the text area
        st.text_area(
            label="Generated Rebuttal",
            value=st.session_state.current_template,
            height=200,
            disabled=False  # This makes it editable
        )
        
        # At the bottom of your main function, add the circles
        circles_html = f"""
            <div class="circle-container">
                {"".join(['<div class="circle"></div>' for _ in range(st.session_state.active_users)])}
            </div>
        """
        st.markdown(circles_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

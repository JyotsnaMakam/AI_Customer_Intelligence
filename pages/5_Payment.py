import streamlit as st
import time

st.set_page_config(page_title="Secure Checkout", layout="centered")

# --- 1. SECURITY CHECK ---
# Ensures the user didn't just type the URL to get here without a product
if "selected_product" not in st.session_state:
    st.warning("⚠️ Your cart is empty! Please select a product from the Marketplace first.")
    if st.button("Back to Marketplace"):
        st.switch_page("pages/4_Marketplace.py")
    st.stop()

st.title("💳 Secure Checkout")
st.write("---")

# --- 2. ORDER SUMMARY ---
st.subheader("Order Summary")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Item:** {st.session_state.selected_product}")
with col2:
    st.write(f"**Total Amount:** :green[{st.session_state.product_price}]")

st.write("---")

# --- 3. UPDATED PAYMENT FORM ---
st.subheader("Payment Method")

with st.form("payment_form"):
    # New Option: Select Card Type
    card_type = st.radio(
        "Select your card type:",
        ["Credit Card 💳", "Debit Card 🏦"],
        horizontal=True
    )
    
    st.write("### Card Details")
    card_name = st.text_input("Name on Card", placeholder="e.g. JYOTSNA")
    card_number = st.text_input("Card Number", placeholder="0000 0000 0000 0000")
    
    c1, c2 = st.columns(2)
    with c1:
        expiry = st.text_input("Expiry Date", placeholder="MM/YY")
    with c2:
        cvv = st.text_input("CVV", type="password", placeholder="***")
    
    # Checkbox for Terms
    agree = st.checkbox("I agree to the terms and conditions of this transaction.")

    submit = st.form_submit_button("Proceed to Pay")

    if submit:
        if not card_name or not card_number or not agree:
            st.error("❌ Please fill in all details and agree to the terms.")
        else:
            # Simulation of a real payment gateway
            with st.status(f"Processing {card_type}...", expanded=True) as status:
                st.write("Connecting to secure server...")
                time.sleep(1.5)
                st.write(f"Verifying {card_type} limits...")
                time.sleep(1.2)
                st.write("Finalizing transaction...")
                time.sleep(1)
                status.update(label="Payment Successful! 🎉", state="complete", expanded=False)
            
            st.balloons()
            st.success(f"Transaction Complete! {st.session_state.selected_product} will be delivered shortly.")
            
            # Clear the 'cart' after success
            del st.session_state.selected_product
            del st.session_state.product_price
            
            if st.button("Back to Dashboard"):
                st.switch_page("main.py")
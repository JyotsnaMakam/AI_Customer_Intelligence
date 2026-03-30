import streamlit as st
import time

st.set_page_config(page_title="Secure Checkout", layout="centered")

# --- 1. INITIALIZE SESSION STATE ---
if 'payment_done' not in st.session_state:
    st.session_state.payment_done = False

# Security check: ensure there is an item to pay for
if "selected_product" not in st.session_state and not st.session_state.payment_done:
    st.warning("⚠️ Your cart is empty!")
    if st.button("Back to Marketplace"):
        st.switch_page("4_Marketplace")
    st.stop()

st.title("💳 Secure Checkout")

# --- 2. SHOW SUCCESS SCREEN IF PAYMENT COMPLETED ---
if st.session_state.payment_done:
    st.balloons()
    st.success("🎉 Transaction Complete! Your order is confirmed.")
    st.info("A receipt has been sent to your registered email.")
    
    # This button is now safe because it's OUTSIDE the form
    if st.button("Return to Home Dashboard"):
        st.session_state.payment_done = False # Reset for next time
        st.switch_page("1_Registration")  # page 1 is the app home / dashboard in this app
    st.stop() # Stop the rest of the script from running

# --- 3. SHOW PAYMENT FORM ---
st.subheader("Order Summary")
st.write(f"**Item:** {st.session_state.get('selected_product', 'None')}")
st.write(f"**Total:** :green[{st.session_state.get('product_price', '$0')}]")
st.write("---")

with st.form("payment_form"):
    st.subheader("Payment Method")
    card_type = st.radio("Select card type:", ["Credit Card 💳", "Debit Card 🏦"], horizontal=True)
    
    card_name = st.text_input("Name on Card")
    card_num = st.text_input("Card Number", placeholder="0000 0000 0000 0000")
    
    c1, c2 = st.columns(2)
    with c1:
        expiry = st.text_input("Expiry (MM/YY)")
    with c2:
        cvv = st.text_input("CVV", type="password")
    
    agree = st.checkbox("I agree to the terms of this transaction.")
    
    # This is the ONLY button allowed in the form
    submit = st.form_submit_button("Confirm & Pay")

    if submit:
        if not card_name or not card_num or not agree:
            st.error("Please fill in all details and agree to terms.")
        else:
            # Simulate processing
            with st.status("Verifying Transaction...", expanded=True) as status:
                time.sleep(2)
                status.update(label="Payment Approved!", state="complete")
            
            # SET THE FLAG AND RERUN
            st.session_state.payment_done = True
            st.rerun()
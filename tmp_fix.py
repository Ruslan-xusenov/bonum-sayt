import os

content = """{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="main-layout">
    <div class="checkout-layout">
        <!-- Checkout Form -->
        <div class="checkout-form-container">
            <h1 style="font-size: 32px; font-weight: 800; margin-bottom: 10px; color: var(--text-main);">Buyurtmani rasmiylashtirish (FIXED V2)</h1>
            <p style="color: var(--text-gray); margin-bottom: 40px;">Yetkazib berish ma'lumotlarini kiriting</p>

            <form action="{% url 'market:checkout' %}" method="POST">
                {% csrf_token %}
                <div class="form-group">
                    <label>1. Ism familiya</label>
                    <input type="text" name="full_name" class="form-input" value="{{ profile.user.first_name }} {{ profile.user.last_name }}" required>
                </div>

                <div class="form-group">
                    <label>2. Telefon raqam</label>
                    <input type="text" name="phone_number" class="form-input" value="{{ profile.phone_number }}" required>
                </div>

                <div class="form-group">
                    <label>3. Manzil</label>
                    <textarea name="address" rows="4" class="form-input" style="resize: none;" required>{{ profile.address }}</textarea>
                </div>

                <button type="submit" class="btn-white" style="width: 100%; padding: 20px; font-size: 18px; border-radius: 12px;">Buyurtma berish</button>
            </form>
        </div>

        <!-- Order Summary -->
        <div class="checkout-summary">
            <h3 style="font-size: 20px; font-weight: 700; margin-bottom: 25px; color: var(--text-main);">Sizning buyurtmangiz</h3>

            <div style="max-height: 400px; overflow-y: auto; margin-bottom: 25px; padding-right: 10px;">
                {% for item in cart_items %}
                <div style="display: flex; gap: 15px; margin-bottom: 20px; align-items: center;">
                    <div style="width: 65px; height: 65px; background: #f8f9fa; border-radius: 14px; overflow: hidden; flex-shrink: 0; border: 1px solid #eee;">
                        {% if item.product.image %}
                        <img src="{{ item.product.image.url }}" style="width: 100%; height: 100%; object-fit: cover;">
                        {% else %}
                        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: #333;">
                            <i class="fas fa-image"></i>
                        </div>
                        {% endif %}
                    </div>
                    <div style="flex: 1;">
                        <h4 style="font-size: 15px; font-weight: 600; color: var(--text-main); margin: 0 0 5px 0;">{{ item.product.name }}</h4>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: var(--text-gray); font-size: 13px;">{{ item.quantity }} x {{ item.product.price|floatformat:0 }} so'm</span>
                            <span style="color: var(--primary-yellow); font-weight: 700; font-size: 14px;">{{ item.total_price|floatformat:0 }} so'm</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>

            <div style="border-top: 1px solid var(--border-color); padding-top: 25px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px; color: var(--text-gray); font-size: 14px;">
                    <span>Jami mahsulotlar:</span>
                    <span style="color: var(--text-main); font-weight: 600;">{{ cart_items|length }} ta</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 25px;">
                    <span style="font-size: 18px; font-weight: 700; color: var(--text-main);">Jami:</span>
                    <span style="font-size: 22px; font-weight: 900; color: var(--primary-yellow);">{{ total_amount|floatformat:0 }} so'm</span>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

with open('templates/market/checkout.html', 'w', encoding='utf-8') as f:
    f.write(content)
"""

with open('tmp_fix.py', 'w', encoding='utf-8') as f:
    f.write(content)

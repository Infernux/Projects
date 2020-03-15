$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, device/oneplus/dumpling/device.mk)

PRODUCT_NAME := op5t_gsi
PRODUCT_DEVICE := op5t_gen
PRODUCT_BRAND := OnePlus_mrnux
PRODUCT_MODEL := Semi gsi op5t

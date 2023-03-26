export default function applyDiscount(price, type, amount) {
    let priceInt = parseInt(price, 10)
    const DiscountType = {
        PRICE_FIX: "fixed_price",
        DISCOUNT_PERCENT: "percentage_discount",
        DISCOUNT_FIX: "fixed_discount",
    }
    if (type === DiscountType.PRICE_FIX) {
        const newPrice = amount;
        return newPrice
    }
    if (type === DiscountType.DISCOUNT_PERCENT) {
        const newPrice = priceInt - priceInt * amount / 100;
        return newPrice
    }
    if (type === DiscountType.DISCOUNT_FIX) {
        const newPrice = priceInt - amount;
        return newPrice
    }

    throw new Error(`Неизвестный тип скидки: ${type}; `);
}
export default class FetchApi {
    static async fetchApi(apiUrl, options = {}) {
        var data = [];
        var status = null;
        try {
            const response = await fetch(apiUrl, options);
            status = response.status
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}; url: ${apiUrl}`);
            }
            data = await response.json();
        } catch (error) {
            if (status == null) {
                status = 500
            }
            console.error(error);
        }
        return {
            data: data,
            status: status
        }
    }

    static async getPromos(userId) {
        const apiUrl = `/api/promo/user/${userId}`;
        return await this.fetchApi(apiUrl);
    }

    static async activatePromo(userId, serviceId, promoCode) {
        const body = {
            user_id: userId,
            service_id: serviceId,
            code: promoCode
        }
        const apiUrl = `/api/promo/activate`;
        const options = {
            method: "POST",
            body: JSON.stringify(body),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }
        return await this.fetchApi(apiUrl, options);
    }

    static async deactivatePromo(userId, promoCode) {
        const body = {
            user_id: userId,
            code: promoCode
        }
        const apiUrl = `/api/promo/deactivate`;
        const options = {
            method: "POST",
            body: JSON.stringify(body),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }
        return await this.fetchApi(apiUrl, options);
    }

    static async getProducts() {
        const apiUrl = `/api/promo/products`;
        return await this.fetchApi(apiUrl);
    }
}
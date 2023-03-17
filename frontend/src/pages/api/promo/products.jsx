import FetchApi from "../../../lib/api/fetchAPi";

export default async function handler(req, res) {
    const baseUrl = process.env.BASE_API_URL;
    const endpoint = "/api/v1/promo/products";
    const apiUrl = `${baseUrl}${endpoint}`

    const options = {
        method: "GET",
    }
    const response = await FetchApi.fetchApi(apiUrl, options);
    res.status(response.status).json(response.data);
}
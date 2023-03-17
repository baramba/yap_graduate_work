import FetchApi from "../../../lib/api/fetchAPi";

export default async function handler(req, res) {
    const baseUrl = process.env.BASE_API_URL;
    const endpoint = "/api/v1/promo/activate";
    const apiUrl = `${baseUrl}${endpoint}`
    const { body } = req;
    const options = {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    }
    const response = await FetchApi.fetchApi(apiUrl, options);
    res.status(response.status).json(response.data);
}
import Error from 'next/error';
import FetchApi from "../../../../lib/api/fetchAPi";

export default async function handler(req, res) {

    const baseUrl = process.env.BASE_API_URL;
    const endpoint = "/api/v1/promo/user";
    const apiUrl = `${baseUrl}${endpoint}`

    const { query } = req;
    const { id } = query;
    const response = await FetchApi.fetchApi(`${apiUrl}/${id}`);
    res.status(response.status).json(response.data);
}

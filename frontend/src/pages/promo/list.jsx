import PromosList from "../../components/promosList";
import Error from 'next/error'
import React from 'react'
import { Stack, TextField, Button, Divider } from "@mui/material";
import FetchApi from "../../lib/api/fetchAPi";


export default function Promos() {
    const [promos, setPromos] = React.useState([]);
    const [userId, setUserId] = React.useState("ee2abd29-4471-af34-e309-e238343c0df0");
    const [response, setResponse] = React.useState([]);

    const getPromos = async () => {
        const resultPromos = await FetchApi.getPromos(userId);
        setPromos(resultPromos.data)
        setResponse(resultPromos)
    };

    const handleUserIdChange = event => {
        setUserId(event.target.value);
    };

    // if (errorCode) {
    //     return <Error statusCode={errorCode} />
    // }
    return (
        <>
            <Stack alignItems="center" justifyContent="flex-end" direction="row" spacing={2} pt={2} pb={2} pr={2}>
                <TextField
                    label="Введите идентификатор пользователя"
                    defaultValue={userId}
                    required
                    onChange={handleUserIdChange}
                    sx={{ width: 500 }}
                />
                <Button onClick={getPromos} size="medium" variant="contained" color="primary">
                    Получить список
                </Button>
            </Stack>
            {promos?.length > 0 && <PromosList data={promos} response={response} />}

        </>
    );
}




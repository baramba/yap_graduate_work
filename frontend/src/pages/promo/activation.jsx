import Link from "next/link";
import React from 'react'
import CheckoutLayout from "../../components/checkoutLayout";
import { Stack, TextField, Button, Typography, Grid, Autocomplete, Alert } from "@mui/material";
import FetchApi from "../../lib/api/fetchAPi";
import TechInfo from "../../components/techInfo";
import applyDiscount from "../../lib/api/utils";


const defaultProduct = {
    "img": "/images/mandalorec.webp",
    "price": "1000.00",
    "name": "Мандалорец",
    "desc": "Одинокий мандалорец-наёмник живёт на краю обитаемой галактики, куда не дотягивается закон Новой Республики. Представитель некогда могучей расы благородных воинов теперь вынужден влачить жалкое существование среди отбросов общества.",
};
const defaultPrice = defaultProduct.price;

const defaultPromoCode = "YAP20";
const defaultUserId = "3fa85f64-5717-4562-b3fc-2c963f66afa6";
const defaultServiceId = "3fa85f64-5717-4562-b3fc-2c963f66afa6";

export default function Activation() {
    const [promoCode, setPromoCode] = React.useState(defaultPromoCode);
    const [userId, setUserId] = React.useState(defaultUserId);
    const [data, setData] = React.useState([]);
    const [product, setProduct] = React.useState(defaultProduct);
    const [isActivate, setActivate] = React.useState(false);
    const [services, setServices] = React.useState([]);
    const [service, setService] = React.useState();
    const [fail, setFail] = React.useState(false);


    React.useEffect(() => {
        const fetchData = async () => {
            const services = await FetchApi.getProducts();
            const serviceApi = services.data.map(({ id, name }) => ({ label: name, id: id }));
            setServices(serviceApi);
        }
        fetchData();
    }, []);


    const activatePromo = async () => {
        const result = await FetchApi.activatePromo(userId, service.id, promoCode);
        setData(result)

        if (result.data.result === false) {
            setFail(true);
            return;
        }
        const newPrice = applyDiscount(product.price, result.data.discount_type, result.data.discount_amount);
        product.price = newPrice;
        setProduct(product);
        setActivate(true);
        setFail(false)
    };

    const deactivatePromo = async () => {
        const result = await FetchApi.deactivatePromo(userId, promoCode);
        setActivate(false);
        setData(result);
        product.price = defaultPrice;
        setProduct(product);
    };

    const handleUserIdChange = event => {
        setUserId(event.target.value);
    };
    const handlePromoCodeChange = event => {
        setPromoCode(event.target.value);
    };
    const handleServiceIdChange = event => {
        setServiceId(event.target.value);
    };


    return (
        <>
            <CheckoutLayout product={product} data={data} />
            <Grid sx={{ pt: 4, pb: 4 }} container alignItems="center" spacing={2}>
                <Grid item xs={4}>
                    <TextField
                        label="Введите идентификатор пользователя"
                        value={userId}
                        required
                        fullWidth
                        onChange={handleUserIdChange}
                    />
                </Grid>
                <Grid item xs={4}>
                    <Autocomplete
                        isOptionEqualToValue={(option, value) => option.id === value.id}
                        disablePortal
                        id="service_id"
                        options={services}
                        onChange={(_, newValue) => {
                            setService(newValue);
                        }}

                        fullWidth
                        renderInput={(params) => <TextField {...params} label="Тип продукта" />}
                    />
                </Grid>
                <Grid item xs={4}>
                    <TextField
                        label="Промокод"
                        defaultValue={promoCode}
                        required
                        fullWidth
                        onChange={handlePromoCodeChange}
                    />
                </Grid>
                <Grid item container xs={12} justifyContent="flex-end">
                    <Button onClick={activatePromo} size="medium" variant="contained" color="primary" disabled={isActivate}>
                        Активировать
                    </Button>
                </Grid>
                {isActivate &&
                    <>
                        <Grid item xs={10}>
                            {/* <Typography variant="body1">Промокод активирован ({promoCode}), тип: {data.data.discount_type}, значение: {data.data.discount_amount}</Typography> */}
                            <Alert severity="success">Промокод активирован ({promoCode}), тип: {data.data.discount_type}, значение: {data.data.discount_amount}</Alert>
                        </Grid>
                        <Grid item container justifyContent="flex-end" xs>
                            <Button onClick={deactivatePromo} size="medium" variant="contained" color="primary">
                                Удалить
                            </Button>
                        </Grid>
                    </>
                }
                {fail &&
                    <Grid item xs={12}>
                        <Alert severity="warning">{data.data.error_message}</Alert>
                    </Grid>
                }
            </Grid>
            <TechInfo data={data} />
        </>
    );
}
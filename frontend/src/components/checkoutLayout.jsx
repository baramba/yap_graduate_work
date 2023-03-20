import Image from "next/image";
import React from "react";
import {
    Card,
    CardContent,
    CardMedia,
    Typography,
} from "@mui/material";
import TechInfo from "./techInfo";



export default function CheckoutPage({ product, data }) {
    return (
        <>
            <Card sx={{ display: "flex" }}>
                {/* <CardMedia component="img" height="194" title={product.name}>
                    <Image
                        // width={500}
                        fill
                        src={product.img}
                        alt="Изображение товара"
                    />
                </CardMedia> */}
                <CardMedia
                    component="img"
                    sx={{ m: 2, width: 600 }}
                    image={product.img}
                    alt="Live from space album cover"
                />

                <CardContent sx={{ display: "flex", flexDirection: "column" }}>
                    <Typography variant="h3" component="h2" sx={{ mb: 1 }}>
                        {product.name}
                    </Typography>
                    <Typography variant="body1" color="text.secondary" sx={{ mb: 1 }}>
                        {product.desc}
                    </Typography>
                    <Typography align="right" variant="h4" sx={{ color: "primary.light" }}>
                        {product.price} руб.
                    </Typography>
                </CardContent>
            </Card>
        </>
    );
}


import React from "react";
import {
    TableContainer,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    Paper,
} from "@mui/material";


export default function PromosList({ data, response}) {
    const columns = Object.keys(data[0]) || []
    return (
        <>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650, maxWidth: 1700 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            {
                                columns.map(column => (
                                    <TableCell key={column}>{column}</TableCell>
                                ))
                            }
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {data.map((item, index) => (
                            <TableRow
                                key={index}
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                {columns.map((column) => (
                                    <TableCell key={column} component="th" scope="row">
                                        {item[column]}
                                    </TableCell>
                                ))}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </>
    );
}

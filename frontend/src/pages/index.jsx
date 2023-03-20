import Head from "next/head";
import Link from "next/link";
import { Typography, Stack, ThemeProvider } from "@mui/material";
import { createTheme } from '@mui/material/styles';
import { grey } from '@mui/material/colors';

const theme = createTheme({
  typography: {
    member: {
      fontSize: 42,
      fontWeight: 300,
      fontFamily: `"Roboto", "Helvetica", "Arial", sans-serif`,
      color: grey[900],
    },
    title: {
      fontSize: 48,
      fontWeight: 300,
      fontFamily: `"Roboto", "Helvetica", "Arial", sans-serif`,
    },
  },
});

export default function HomePage() {
  return (
    <>
      <ThemeProvider theme={theme}>
        <Head>
          <title>Демонстрационная страница сервиса лояльности.</title>

        </Head>
        <Typography variant="title">Команда дипломного проекта</Typography>
        <Stack sx={{ m: 3 }}>
          <Typography variant="member">Антон Ревуцкий, backend</Typography>
          <Typography variant="member">Юрий Сухобок, backend</Typography>
          <Typography variant="member">Михаил  Индуров, backend</Typography>
          <Typography variant="member" >Бабихин Максим, frontend</Typography>
        </Stack>
      </ThemeProvider>
    </>
  );
}




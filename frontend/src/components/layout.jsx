// import Navbar from './navbar'
// import Footer from './footer'
import { Paper, Container, Drawer, Typography, AppBar, Toolbar, Divider, List, ListItem, ListItemButton, ListItemText, Box } from "@mui/material"
import Link from 'next/link'

const drawerWidth = 300;


const pages = [
    { "path": "/promo/activation", "name": "Активация промокода" },
    { "path": "/promo/list", "name": "Список промокодов пользователя" },
    // { "path": "/promo/list2", "name": "Не подходящий типа сервиса" },
    // { "path": "/promo/list3", "name": "Истекший срок годности" },
    // { "path": "/promo/list4", "name": "Многоразовый промокод" },
]

export default function Layout({ children }) {
    return (
        <>
            <AppBar
                position="fixed"
                sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
            >
                <Toolbar>
                    <Typography variant="h6" noWrap component="div">
                        Сервис лояльности
                    </Typography>
                </Toolbar>
            </AppBar>
            <Drawer
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    '& .MuiDrawer-paper': {
                        width: drawerWidth,
                        boxSizing: 'border-box',
                    },
                }}
                variant="permanent"
                anchor="left"
            >
                <Toolbar />
                <List>
                    <ListItem key="home" disablePadding>
                        <ListItemButton component={Link} href="/" >
                            <ListItemText primary="Главная" />
                        </ListItemButton>
                    </ListItem>
                </List>
                <Divider />
                <List>
                    {pages.map((page) => (
                        <ListItem key={page.path} disablePadding>
                            <ListItemButton component={Link} href={page.path}>
                                <ListItemText primary={page.name} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
                <Divider />

            </Drawer>
            <Toolbar />
            <Box sx={{ ml: 30 }}>
                <Container maxWidth="xl">
                    {/* <Paper> */}
                    <main>{children}</main>
                    {/* </Paper> */}
                </Container>
            </Box>
        </>
    )
}
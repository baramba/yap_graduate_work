import { AppProps } from 'next/app'
import Layout from '../components/layout'

export default function MyApp({ Component, pageProps }) {
    return (
        <Layout>
            <Component {...pageProps} />
        </Layout>
    )
}

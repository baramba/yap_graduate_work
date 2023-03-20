import { rest } from "msw";
import { setupServer } from "msw/node";
import { setupWorker } from 'msw'
import OpenAPIBackend from "openapi-backend";


// create our mock backend with openapi-backend
const api = new OpenAPIBackend({ definition: './promos.json' });

api.register("notFound", (c, res, ctx) => res(ctx.status(404)));
api.register("notImplemented", async (c, res, ctx) => {
    const { status, mock } = api.mockResponseForOperation(
        c.operation.operationId
    );
    ctx.status(status);
    return res(ctx.json(mock));
});


const handlers = [
    // rest.all("/api/*", async (req, res, ctx) =>
    //     api.handleRequest(
    //         {
    //             path: req.url.pathname,
    //             query: req.url.search,
    //             method: req.method,
    //             body: req.bodyUsed ? await req.json() : null,
    //             headers: { ...req.headers.raw },
    //         },
    //         res,
    //         ctx
    //     )
    // ),
    rest.get('http://localhost:3000/reviews', (_req, res, ctx) => {
        return res(
            ctx.json([
                {
                    id: '60333292-7ca1-4361-bf38-b6b43b90cb16',
                    author: 'John Maverick',
                    text: 'Lord of The Rings, is with no absolute hesitation, my most favored and adored book by‑far. The trilogy is wonderful‑ and I really consider this a legendary fantasy series. It will always keep you at the edge of your seat‑ and the characters you will grow and fall in love with!',
                },
            ])
        )
    }),
]


async function initMocks() {
    if (typeof window === 'undefined') {
        const server = setupServer(...handlers)
        server.listen()
    } else {
        const worker = setupWorker(...handlers);
        worker.start()
    }
}

initMocks()

export { }

// beforeAll(() => server.listen());
// afterAll(() => server.close());
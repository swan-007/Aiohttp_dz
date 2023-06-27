import json

from aiohttp import web


from models import Advertisement, Base, Session, engine

app = web.Application()

@web.middleware
async def session_middleware(request: web.Request, handler):
    print('m_start')
    async with Session() as session:
        request["session"] = session
        resource = await handler(request)
        print('m_end')
        return resource


async def get_advertisement(advertisement_id: int, s: Session):
    advertisement = await s.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise web.HTTPNotFound(content_type='application/json', text=json.dumps({
                'error': 'adtv not found '
            }))
    return advertisement


class AdvertisementApiView(web.View):

    def session(self):
        return self.request["session"]

    @property
    def advertisement_id(self):
        return int(self.request.match_info["post_id"])

    async def get(self):
        advertisement = await get_advertisement(self.advertisement_id, self.session())
        return web.json_response({'id': advertisement.id})

    async def post(self):
        json_data = await self.request.json()
        advertisement = Advertisement(**json_data)
        self.session().add(advertisement)
        await self.session().commit()
        return web.json_response(
            {"id": advertisement.id})


    async def patch(self):
        json_data = await self.request.json()
        advertisement = await get_advertisement(self.advertisement_id, self.session())
        for key, val in json_data.items():
            setattr(advertisement, key, val)
        self.session().add(advertisement)
        await self.session().commit()
        return web.json_response({'id': advertisement.id})


    async def delete(self):
        advertisement = await get_advertisement(self.advertisement_id, self.session())
        await self.session().delete(advertisement)
        await self.session().commit()
        return web.json_response({'id': advertisement.id})


async def orm_context(app: web.Application):
    print('Start')
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    yield
    print('END')
    await engine.dispose()


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)
app.add_routes(
    [
        web.post("/api/", AdvertisementApiView),
        web.get("/api/{post_id:\d+}", AdvertisementApiView),
        web.patch("/api/{post_id:\d+}", AdvertisementApiView),
        web.delete("/api/{post_id:\d+}", AdvertisementApiView),
    ]
)


if __name__ == "__main__":

    web.run_app(app)

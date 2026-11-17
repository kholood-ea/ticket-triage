import uvicorn
import logging

from fastapi import FastAPI, HTTPException

from . import db
from .config import get_settings
from .logging_config import setup_logging
from .schemas import CategoryCount, TicketIn, TicketOut

log = logging.getLogger("ticket_service")


def create_app(db_path: str | None = None) -> FastAPI:
    settings = get_settings()
    setup_logging(settings.log_level)
    path = db_path or settings.db_path
    db.init_db(path)

    app = FastAPI(title="Arabic Ticket Triage")

    @app.post("/tickets", response_model=TicketOut, status_code=201)
    def create_ticket(ticket: TicketIn):
        tid = db.insert_ticket(path, ticket.text, ticket.channel.value, ticket.metadata)
        # Log lengths and ids, never raw ticket text (it may contain PII).
        log.info("ticket_created", extra={"ctx": {"ticket_id": tid, "text_len": len(ticket.text), "channel": ticket.channel.value}})
        return db.get_ticket(path, tid)

    @app.get("/tickets/{ticket_id}", response_model=TicketOut)
    def read_ticket(ticket_id: int):
        row = db.get_ticket(path, ticket_id)
        if row is None:
            raise HTTPException(status_code=404, detail="ticket not found")
        return row

    @app.get("/stats/by-category", response_model=list[CategoryCount])
    def stats_by_category():
        return db.counts_by_category(path)

    return app


app = create_app()
DROP TRIGGER IF EXISTS trg_notify_transaction

ON daily_trn;


CREATE TRIGGER trg_notify_transaction

AFTER INSERT

ON daily_trn

FOR EACH ROW

EXECUTE FUNCTION notify_new_transaction();
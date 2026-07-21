CREATE OR REPLACE FUNCTION notify_new_transaction()

RETURNS trigger

AS $$

BEGIN

    PERFORM pg_notify(

        'new_transaction',

        NEW.comp_cd || '|' ||

        NEW.branch_cd || '|' ||

        NEW.tran_cd || '|' ||

        NEW.tran_dt

    );

    RETURN NEW;

END;

$$ LANGUAGE plpgsql;
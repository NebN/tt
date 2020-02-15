import traceback
from timeit import default_timer as timer
from datetime import timedelta
from rply.errors import LexingError
from src.lang import compile_transformation
from src.model import Text
from src.util import TimeUtils


class Controller:

    def __init__(self, worksheet):
        self.worksheet = worksheet

        # declaring this outside __init__ does not work, why?
        def _handleexecute(code):
            transformation = None

            try:
                transformation = compile_transformation(code)
            except LexingError as e:
                self.worksheet.setmessage(f'syntax error at index {e.source_pos.idx}')
                print(e)
                print(traceback.format_exc())
            except ValueError as e:
                self.worksheet.setmessage('syntax error')
                print(e)
                print(traceback.format_exc())
            except Exception as e:
                self.worksheet.setmessage('unknown error')
                print(e)
                print(traceback.format_exc())

            if transformation:
                input = Text(text=self.worksheet.getinput())
                self.worksheet.setmessage('executing...')
                t0 = timer()
                output = None
                try:
                    output = transformation.transform(input).text()
                except Exception as e:
                    self.worksheet.setmessage(f'error while transforming: {e}')

                t1 = timer()
                elapsed = timedelta(seconds=(t1 - t0))
                self.worksheet.setmessage(f'transformed in {(TimeUtils.timedelta_to_string(elapsed))}')
                self.worksheet.setoutput(output)

        self.worksheet.run.connect(_handleexecute)

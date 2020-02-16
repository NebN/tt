import traceback
from timeit import default_timer as timer
from datetime import timedelta
from rply.errors import LexingError
from src.lang import compile_transformation
from src.model import Text
from src.util import TimeUtils
from src.gui import Color


class Controller:

    def __init__(self, worksheet):
        self.worksheet = worksheet

        # declaring this outside __init__ does not work, why?
        def _handleexecute(code):
            transformation = None
            try:
                transformation = compile_transformation(code)
                self.worksheet.last_execution_code = self.worksheet.code.get()
            except LexingError as e:
                ix = e.source_pos.idx
                worksheet.code.flash(Color.RED)
                text = worksheet.code.document().findBlock(ix).text()
                self.worksheet.setmessage(f'syntax error: {text}')
                self.worksheet.highlighter.error(ix, len(text))
                print(e)
                # print(traceback.format_exc())
            except ValueError as e:
                worksheet.code.flash(Color.RED)
                self.worksheet.setmessage(f'syntax error: {e}')
                print(e)
                # print(traceback.format_exc())
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
                self.worksheet.output.flash(Color.GREEN, end=Color.DARK_GREEN)
                self.worksheet.setoutput(output)

        self.worksheet.run.connect(_handleexecute)

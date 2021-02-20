from idewavecore.session import Storage, ItemFlag


async def mock_middleware(**kwargs):
    session_storage: Storage = kwargs.pop('session_storage')
    mock_value: int = session_storage.get_value('mock_value') or 0
    mock_value += 1

    session_storage.set_items([
        {
            'mock_value': {
                'value': mock_value,
                'flags': ItemFlag.PERSISTENT
            }
        }
    ])

    break_after = session_storage.get_value('break_after')
    if break_after and mock_value >= break_after:
        session_storage.set_items([
            {
                'should_break': {
                    'value': True,
                    'flags': ItemFlag.PERSISTENT
                }
            }
        ])

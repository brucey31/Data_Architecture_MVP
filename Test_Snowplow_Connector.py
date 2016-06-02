from snowplow_tracker import Subject, Tracker, Emitter
from snowplow_tracker import SelfDescribingJson

e = Emitter("d3rkrsqld9gmqf.cloudfront.net")



t = Tracker(e)
s = Subject()
s.set_user_id( "{{USER ID}}" )


t.track_unstruct_event(SelfDescribingJson(
  "com.example_company/save-game/jsonschema/1-0-2",
  {
    "save_id": "4321",
    "level": 23,
    "difficultyLevel": "HARD",
    "dl_content": True
  }
)
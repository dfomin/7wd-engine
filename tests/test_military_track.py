from swd.military_track import MilitaryTrack


def test_military_supremacist():
    track = MilitaryTrack(9, [False] * 4)
    assert track.military_supremacist == 0

    track = MilitaryTrack(-9, [False] * 4)
    assert track.military_supremacist == 1

    track = MilitaryTrack()
    track.apply_shields(0, 9, lambda x, y: None)
    assert track.military_supremacist == 0

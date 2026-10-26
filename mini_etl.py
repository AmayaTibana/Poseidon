"""
================================================================================
 PYTHON FROM PSEUDOCODE - Mini ETL Workbook: "Music Streams"
================================================================================

HOW TO USE
  1. Read the PSEUDOCODE in each task's docstring.
  2. Delete the `raise NotImplementedError` line and write the Python yourself.
  3. Run the checker:
         python streams_workbook.py        -> checks every task
         python streams_workbook.py 7      -> checks only task 7
  4. Each task shows PASS, FAIL (wrong answer), ERROR (crashed) or TODO.

RULES
  - Standard library only (no pandas). The point is to practice core Python.
  - Do the tasks in order. Later tasks reuse earlier functions.
  - Don't change the function names or parameters (the checker uses them).
  - Stuck for more than 20 minutes? Read the HINT line, look up the keyword
    in the Python docs, then try again before searching for a full answer.

PSEUDOCODE KEYWORDS
  SET x TO ...       -> x = ...
  FOR EACH item IN   -> for item in ...:
  IF / ELSE IF / ELSE-> if / elif / else
  RETURN             -> return
  APPEND x TO list   -> my_list.append(x)

LEVELS
  Level 1  Warm-up            Tasks 1-3   (math, strings, conditionals)
  Level 2  Lists & dicts      Tasks 4-6   (the core data structures)
  Level 3  Extract            Task 7      (read CSV text)
  Level 4  Transform          Tasks 8-10  (clean, dedupe, parse dates)
  Level 5  Aggregate          Tasks 11-13 (GROUP BY, but in Python)
  Level 6  Load + pipeline    Tasks 14-15 (write a file, wire it all up)
================================================================================
"""

import csv
import io
import os
import sys
import tempfile
from datetime import datetime


# ------------------------------------------------------------------------------
# RAW DATA (intentionally messy, like real source data)
#   - inconsistent casing ("Pop", "POP", "pop")
#   - extra spaces ("  Levitating ")
#   - a duplicate row (stream_id 4)
#   - bad values (duration "abc", duration 0, empty track)
# ------------------------------------------------------------------------------
RAW_CSV = """stream_id,user_id,track,artist,genre,duration_sec,played_at,country
1,u01,Blinding Lights,The Weeknd,Pop,200,2026-10-01 08:15:00,us
2,u01,  Levitating ,Dua Lipa,POP,203,2026-10-01 08:20:00,US
3,u02,Titi Me Pregunto,Bad Bunny,Reggaeton,243,2026-10-01 21:02:00,pr
4,u02,Titi Me Pregunto,Bad Bunny,reggaeton,243,2026-10-01 21:07:00,PR
4,u02,Titi Me Pregunto,Bad Bunny,reggaeton,243,2026-10-01 21:07:00,PR
5,u03,Blinding Lights,The Weeknd,pop,abc,2026-10-01 13:40:00,ca
6,u03,,Unknown,pop,180,2026-10-01 13:45:00,ca
7,u03,Flowers,Miley Cyrus,Pop,0,2026-10-01 13:50:00,ca
8,u01,Blinding Lights,the weeknd,pop,200,2026-10-02 08:30:00,US
9,u04,Ojitos Lindos,Bad Bunny,Reggaeton,258,2026-10-02 21:30:00,mx
10,u04,As It Was,Harry Styles,Pop,167,2026-10-02 22:10:00,mx
11,u02,Monaco,Bad Bunny,Reggaeton,267,2026-10-03 08:05:00,pr
12,u05,Bohemian Rhapsody,Queen,Rock,354,2026-10-03 17:45:00,gb
"""


# ==============================================================================
# LEVEL 1 - WARM-UP
# ==============================================================================

def seconds_to_minutes(seconds):
    """
    TASK 1: Turn a number of seconds into a "m:ss" string.
      seconds_to_minutes(200) -> "3:20"
      seconds_to_minutes(65)  -> "1:05"
      seconds_to_minutes(0)   -> "0:00"

    PSEUDOCODE
      SET minutes TO seconds divided by 60, keeping only the whole number
      SET remaining TO the remainder of seconds divided by 60
      RETURN minutes, a colon, then remaining padded to 2 digits

    HINT: //  %  and f-strings ( f"{x:02d}" pads with a zero )
    """
    minutes = seconds // 60
    remaining = seconds % 60
    return f"{minutes}:{remaining:02d}" #Explain what this line does #copilot do it
    raise NotImplementedError


def classify_duration(seconds):
    if seconds < 120:
        return "short"
    elif seconds >= 120 and seconds <= 300:
        return "normal"
    else:
        return "long"
    """
    TASK 2: Label a song by length.
      under 120 seconds         -> "short"
      120 to 300 (inclusive)    -> "normal"
      over 300                  -> "long"

    PSEUDOCODE
      IF seconds is less than 120
          RETURN "short"
      ELSE IF seconds is less than or equal to 300
          RETURN "normal"
      ELSE
          RETURN "long"

    HINT: if / elif / else
    """
    raise NotImplementedError



def count_vowels(text):
    count = 0
    for char in text.lower():
        if char in "aeiou":
            count += 1
    return count 
    """
    
    TASK 3: Count the vowels (a, e, i, o, u) in text, ignoring upper/lower case.
      count_vowels("Bad Bunny") -> 2

    PSEUDOCODE
      SET count TO 0
      FOR EACH character IN text converted to lowercase
          IF character is one of "aeiou"
              ADD 1 TO count
      RETURN count

    HINT: .lower()  and the  in  operator
    """
    raise NotImplementedError


# ==============================================================================
# LEVEL 2 - LISTS & DICTIONARIES
# ==============================================================================

def unique_in_order(items):
    seen = set[]
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
    
    """
    TASK 4: Remove duplicates but KEEP the original order.
      unique_in_order(["pop", "rock", "pop", "jazz"]) -> ["pop", "rock", "jazz"]
      (SQL idea: SELECT DISTINCT, but order matters)

    PSEUDOCODE
      SET seen TO an empty set
      SET result TO an empty list
      FOR EACH item IN items
          IF item is NOT in seen
              ADD item TO seen
              APPEND item TO result
      RETURN result

    HINT: set(), .add(), .append()
    
    """

    raise NotImplementedError


def count_by(items):
    
    counts = []
    for item in items:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    """
    TASK 5: Count how many times each value appears.
      count_by(["pop", "rock", "pop"]) -> {"pop": 2, "rock": 1}
      (SQL idea: SELECT value, COUNT(*) ... GROUP BY value)

    PSEUDOCODE
      SET counts TO an empty dictionary
      FOR EACH item IN items
          IF item is already a key in counts
              ADD 1 TO counts[item]
          ELSE
              SET counts[item] TO 1
      RETURN counts

    HINT: dict, or counts.get(item, 0) + 1   (don't use collections.Counter yet)
    """
    raise NotImplementedError


def top_n(counts, n):
    """
    TASK 6: Return the n biggest entries of a dict as a list of (key, value) tuples.
      Sort by value DESCENDING; break ties by key ASCENDING (A before B).
      top_n({"a": 1, "b": 3, "c": 3}, 2) -> [("b", 3), ("c", 3)]
      (SQL idea: ORDER BY value DESC, key ASC LIMIT n)

    PSEUDOCODE
      SET pairs TO the list of (key, value) pairs from counts
      SORT pairs by: negative value first, then key
      RETURN the first n pairs

    HINT: .items(), sorted(..., key=lambda pair: (-pair[1], pair[0])), slicing [:n]
    """
    raise NotImplementedError


# ==============================================================================
# LEVEL 3 - EXTRACT
# ==============================================================================

def read_csv_rows(text):
    """
    TASK 7: Turn CSV text into a list of dictionaries (one dict per row).
      The header line becomes the keys. All values stay as strings for now.
      First row of RAW_CSV -> {"stream_id": "1", "user_id": "u01", "track": "Blinding Lights", ...}

    PSEUDOCODE
      WRAP text so it can be read like a file
      CREATE a CSV dictionary reader on it
      SET rows TO an empty list
      FOR EACH row IN the reader
          APPEND row (as a plain dict) TO rows
      RETURN rows

    HINT: io.StringIO(text), csv.DictReader(...), dict(row)
    """
    raise NotImplementedError


# ==============================================================================
# LEVEL 4 - TRANSFORM
# ==============================================================================

def clean_row(row):
    """
    TASK 8: Clean ONE raw row. Return a new cleaned dict, or None if the row is bad.

    Cleaning rules:
      - strip spaces from the start/end of EVERY value
      - artist   -> Title Case          ("the weeknd" -> "The Weeknd")
      - genre    -> lowercase           ("POP" -> "pop")
      - country  -> UPPERCASE           ("us" -> "US")
      - duration_sec -> int             ("200" -> 200)
    Reject (return None) if:
      - track is empty after stripping
      - duration_sec can't be turned into an int  ("abc")
      - duration_sec is 0 or negative

    PSEUDOCODE
      SET clean TO an empty dictionary
      FOR EACH key, value IN row
          SET clean[key] TO value with spaces stripped

      IF clean["track"] is empty
          RETURN None

      TRY
          SET clean["duration_sec"] TO clean["duration_sec"] converted to int
      IF that conversion fails
          RETURN None

      IF clean["duration_sec"] is less than or equal to 0
          RETURN None

      SET clean["artist"]  TO title case of clean["artist"]
      SET clean["genre"]   TO lowercase of clean["genre"]
      SET clean["country"] TO uppercase of clean["country"]
      RETURN clean

    HINT: .strip(), .title(), .lower(), .upper(), try / except ValueError
    """
    raise NotImplementedError


def deduplicate(rows, key="stream_id"):
    """
    TASK 9: Remove duplicate rows based on one column. Keep the FIRST one seen.
      (Same idea as Task 4, but on dicts.)

    PSEUDOCODE
      SET seen_ids TO an empty set
      SET result TO an empty list
      FOR EACH row IN rows
          SET row_id TO row[key]
          IF row_id is NOT in seen_ids
              ADD row_id TO seen_ids
              APPEND row TO result
      RETURN result
    """
    raise NotImplementedError


def get_hour(played_at):
    """
    TASK 10: Pull the hour (0-23) out of a timestamp string.
      get_hour("2026-10-01 21:02:00") -> 21
      (SQL idea: EXTRACT(HOUR FROM played_at))

    PSEUDOCODE
      PARSE played_at into a datetime using the format "year-month-day hour:minute:second"
      RETURN the hour of that datetime

    HINT: datetime.strptime(text, "%Y-%m-%d %H:%M:%S").hour
    """
    raise NotImplementedError


# ==============================================================================
# LEVEL 5 - AGGREGATE  (GROUP BY in plain Python)
# ==============================================================================

def total_minutes_by_artist(rows):
    """
    TASK 11: Total listening minutes per artist, rounded to 2 decimals.
      rows are CLEAN rows (duration_sec is already an int).
      (SQL: SELECT artist, ROUND(SUM(duration_sec) / 60.0, 2) ... GROUP BY artist)

    PSEUDOCODE
      SET seconds_by_artist TO an empty dictionary
      FOR EACH row IN rows
          ADD row["duration_sec"] TO seconds_by_artist[row["artist"]]
              (start at 0 if the artist isn't there yet)

      SET result TO an empty dictionary
      FOR EACH artist, seconds IN seconds_by_artist
          SET result[artist] TO seconds divided by 60, rounded to 2 decimals
      RETURN result

    HINT: .get(key, 0), round(number, 2)
    """
    raise NotImplementedError


def plays_by_hour(rows):
    """
    TASK 12: Count plays per hour of the day.
      Returns {hour: count}, e.g. {8: 4, 21: 3, ...}

    PSEUDOCODE
      SET hours TO an empty list
      FOR EACH row IN rows
          APPEND get_hour(row["played_at"]) TO hours
      RETURN count_by(hours)

    HINT: you already wrote both helpers (Tasks 5 and 10). Reuse them.
    """
    raise NotImplementedError


def user_summary(rows):
    """
    TASK 13: One summary dict per user.
      {
        "u01": {"plays": 3, "unique_tracks": 2, "top_genre": "pop"},
        ...
      }
      top_genre = the genre that user played most. Ties -> alphabetically first.

    PSEUDOCODE
      SET rows_by_user TO an empty dictionary   (user_id -> list of rows)
      FOR EACH row IN rows
          IF row["user_id"] is not a key yet
              SET rows_by_user[row["user_id"]] TO an empty list
          APPEND row TO rows_by_user[row["user_id"]]

      SET result TO an empty dictionary
      FOR EACH user_id, user_rows IN rows_by_user
          SET plays TO the number of user_rows
          SET tracks TO the set of row["track"] for each row in user_rows
          SET genre_counts TO count_by( the list of row["genre"] for each row in user_rows )
          SET top_genre TO the key of the first pair in top_n(genre_counts, 1)
          SET result[user_id] TO {"plays": plays,
                                  "unique_tracks": number of tracks,
                                  "top_genre": top_genre}
      RETURN result

    HINT: list comprehensions:  [row["genre"] for row in user_rows]
          top_n(...) returns [(key, value)], so [0][0] gets the key
    """
    raise NotImplementedError


# ==============================================================================
# LEVEL 6 - LOAD + FULL PIPELINE
# ==============================================================================

def write_csv(rows, path, columns):
    """
    TASK 14: Write rows (list of dicts) to a CSV file with a header line.
      Only write the given columns, in that order. Return how many rows were written
      (not counting the header).

    PSEUDOCODE
      OPEN the file at path for writing (newline="" and encoding="utf-8")
          CREATE a CSV dictionary writer with fieldnames = columns
              (tell it to ignore keys that aren't in columns)
          WRITE the header
          FOR EACH row IN rows
              WRITE row
      RETURN the number of rows

    HINT: with open(...) as f:   csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
          .writeheader(), .writerow(row), len(rows)
    """
    raise NotImplementedError


def run_pipeline(raw_text, out_path):
    """
    TASK 15: Wire everything together. Extract -> Transform -> Load -> Report.
      Return a summary dict:
        {
          "raw_rows":     how many rows came in,
          "clean_rows":   how many rows survived cleaning AND dedup,
          "dropped":      raw_rows - clean_rows,
          "top_artist":   artist with the most total minutes,
          "busiest_hour": hour with the most plays,
        }

    PSEUDOCODE
      -- EXTRACT
      SET raw TO read_csv_rows(raw_text)

      -- TRANSFORM
      SET cleaned TO an empty list
      FOR EACH row IN raw
          SET c TO clean_row(row)
          IF c is not None
              APPEND c TO cleaned
      SET final_rows TO deduplicate(cleaned)

      -- LOAD
      SET columns TO ["stream_id", "user_id", "track", "artist", "genre",
                      "duration_sec", "played_at", "country"]
      CALL write_csv(final_rows, out_path, columns)

      -- REPORT
      SET top_artist   TO the key of the first pair in top_n(total_minutes_by_artist(final_rows), 1)
      SET busiest_hour TO the key of the first pair in top_n(plays_by_hour(final_rows), 1)
      RETURN the summary dict described above
    """
    raise NotImplementedError


# ==============================================================================
#  CHECKER - you don't need to edit anything below this line
# ==============================================================================

def _test_1():
    assert seconds_to_minutes(200) == "3:20", f"200 -> {seconds_to_minutes(200)!r}"
    assert seconds_to_minutes(65) == "1:05", f"65 -> {seconds_to_minutes(65)!r}"
    assert seconds_to_minutes(59) == "0:59"
    assert seconds_to_minutes(0) == "0:00"


def _test_2():
    for sec, want in [(119, "short"), (120, "normal"), (300, "normal"), (301, "long")]:
        got = classify_duration(sec)
        assert got == want, f"{sec} -> {got!r}, expected {want!r}"


def _test_3():
    assert count_vowels("Bad Bunny") == 2
    assert count_vowels("AEIOU xyz") == 5
    assert count_vowels("") == 0


def _test_4():
    assert unique_in_order(["pop", "rock", "pop", "jazz"]) == ["pop", "rock", "jazz"]
    assert unique_in_order([3, 1, 3, 3, 2, 1]) == [3, 1, 2]
    assert unique_in_order([]) == []


def _test_5():
    assert count_by(["pop", "rock", "pop"]) == {"pop": 2, "rock": 1}
    assert count_by([]) == {}


def _test_6():
    assert top_n({"a": 1, "b": 3, "c": 3}, 2) == [("b", 3), ("c", 3)]
    assert top_n({"x": 5, "y": 9}, 1) == [("y", 9)]
    assert top_n({"x": 5}, 10) == [("x", 5)]


def _test_7():
    rows = read_csv_rows(RAW_CSV)
    assert isinstance(rows, list), "should return a list"
    assert len(rows) == 13, f"expected 13 rows, got {len(rows)}"
    assert rows[0]["track"] == "Blinding Lights"
    assert rows[0]["duration_sec"] == "200", "values should still be strings here"
    assert type(rows[0]) is dict, "each row should be a plain dict"


def _test_8():
    raw = {"stream_id": " 8 ", "user_id": "u01", "track": "  Levitating ",
           "artist": "dua lipa", "genre": "POP", "duration_sec": " 203 ",
           "played_at": "2026-10-01 08:20:00", "country": "us"}
    c = clean_row(raw)
    assert c is not None, "a valid row returned None"
    assert c["stream_id"] == "8"
    assert c["track"] == "Levitating", f"track -> {c['track']!r}"
    assert c["artist"] == "Dua Lipa"
    assert c["genre"] == "pop"
    assert c["country"] == "US"
    assert c["duration_sec"] == 203 and isinstance(c["duration_sec"], int)
    assert raw["track"] == "  Levitating ", "don't modify the original row; build a new dict"
    assert clean_row(dict(raw, duration_sec="abc")) is None, "bad duration should return None"
    assert clean_row(dict(raw, duration_sec="0")) is None, "zero duration should return None"
    assert clean_row(dict(raw, track="   ")) is None, "empty track should return None"


def _test_9():
    rows = [{"stream_id": "1", "v": "a"}, {"stream_id": "2", "v": "b"},
            {"stream_id": "1", "v": "c"}]
    out = deduplicate(rows)
    assert [r["v"] for r in out] == ["a", "b"], f"got {out}"
    out2 = deduplicate([{"k": "x", "v": 1}, {"k": "x", "v": 2}], key="k")
    assert len(out2) == 1 and out2[0]["v"] == 1


def _test_10():
    assert get_hour("2026-10-01 21:02:00") == 21
    assert get_hour("2026-10-03 08:05:00") == 8
    assert isinstance(get_hour("2026-10-01 00:00:00"), int)


def _sample_clean_rows():
    return [
        {"user_id": "u1", "track": "A", "artist": "X", "genre": "pop",  "duration_sec": 200, "played_at": "2026-10-01 08:00:00"},
        {"user_id": "u1", "track": "A", "artist": "X", "genre": "pop",  "duration_sec": 200, "played_at": "2026-10-01 08:30:00"},
        {"user_id": "u1", "track": "B", "artist": "Y", "genre": "rock", "duration_sec": 100, "played_at": "2026-10-01 21:00:00"},
        {"user_id": "u2", "track": "C", "artist": "Y", "genre": "rock", "duration_sec": 50,  "played_at": "2026-10-01 08:10:00"},
        {"user_id": "u2", "track": "D", "artist": "X", "genre": "jazz", "duration_sec": 70,  "played_at": "2026-10-01 21:10:00"},
    ]


def _test_11():
    got = total_minutes_by_artist(_sample_clean_rows())
    assert got == {"X": 7.83, "Y": 2.5}, f"got {got}"


def _test_12():
    got = plays_by_hour(_sample_clean_rows())
    assert got == {8: 3, 21: 2}, f"got {got}"


def _test_13():
    got = user_summary(_sample_clean_rows())
    want = {"u1": {"plays": 3, "unique_tracks": 2, "top_genre": "pop"},
            "u2": {"plays": 2, "unique_tracks": 2, "top_genre": "jazz"}}
    assert got == want, f"got {got}"


def _test_14():
    rows = [{"a": 1, "b": "x", "extra": "ignore me"}, {"a": 2, "b": "y", "extra": "!"}]
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "out.csv")
        n = write_csv(rows, path, ["a", "b"])
        assert n == 2, f"should return 2, got {n}"
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    assert lines == ["a,b", "1,x", "2,y"], f"file contents: {lines}"


def _test_15():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "clean_streams.csv")
        summary = run_pipeline(RAW_CSV, path)
        assert os.path.exists(path), "the clean CSV file was not written"
        with open(path, encoding="utf-8") as f:
            written = list(csv.DictReader(f))
    want = {"raw_rows": 13, "clean_rows": 9, "dropped": 4,
            "top_artist": "Bad Bunny", "busiest_hour": 8}
    assert summary == want, f"got {summary}\n           expected {want}"
    assert len(written) == 9, f"file has {len(written)} rows, expected 9"


TESTS = [
    (1, "seconds_to_minutes", _test_1),
    (2, "classify_duration", _test_2),
    (3, "count_vowels", _test_3),
    (4, "unique_in_order", _test_4),
    (5, "count_by", _test_5),
    (6, "top_n", _test_6),
    (7, "read_csv_rows", _test_7),
    (8, "clean_row", _test_8),
    (9, "deduplicate", _test_9),
    (10, "get_hour", _test_10),
    (11, "total_minutes_by_artist", _test_11),
    (12, "plays_by_hour", _test_12),
    (13, "user_summary", _test_13),
    (14, "write_csv", _test_14),
    (15, "run_pipeline", _test_15),
]


def main():
    only = None
    if len(sys.argv) > 1:
        try:
            only = int(sys.argv[1])
        except ValueError:
            print("Usage: python streams_workbook.py [task_number]")
            return

    passed = 0
    selected = [t for t in TESTS if only is None or t[0] == only]
    if not selected:
        print(f"No task number {only}. Choose 1-{len(TESTS)}.")
        return

    print()
    for num, name, test in selected:
        label = f"Task {num:>2}  {name:<25}"
        try:
            test()
            print(f"  PASS   {label}")
            passed += 1
        except NotImplementedError:
            print(f"  TODO   {label}")
        except AssertionError as e:
            print(f"  FAIL   {label} -> {e}")
        except Exception as e:
            print(f"  ERROR  {label} -> {type(e).__name__}: {e}")

    print(f"\n  Score: {passed}/{len(selected)}")
    if only is None and passed == len(TESTS):
        print("  All done. Your mini ETL pipeline works end to end.")
    print()


if __name__ == "__main__":
    main()
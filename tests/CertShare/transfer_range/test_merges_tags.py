#!/usr/bin/python3

import pytest

from brownie import accounts


@pytest.fixture(scope="module", autouse=True)
def setup(approve_many, nft):
    nft.mint(accounts[1], 10000, 0, "0x00", {"from": accounts[0]})
    nft.mint(accounts[2], 10000, 0, "0x00", {"from": accounts[0]})
    nft.mint(accounts[3], 10000, 0, "0x00", {"from": accounts[0]})


def test_inside(check_ranges, nft):
    """inside"""
    nft.modifyRanges(12000, 13000, 0, "0x01", {"from": accounts[0]})
    check_ranges(
        [(1, 10001)],
        [(10001, 12000), (12000, 13000), (13000, 20001)],
        [(20001, 30001)],
        [],
        tags=True,
    )


def test_start_partial_different(check_ranges, nft):
    """partial, touch start, no merge"""
    nft.modifyRanges(8000, 12000, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[4], 10001, 11001, {"from": accounts[2]})
    check_ranges(
        [(1, 8000), (8000, 10001)],
        [(11001, 12000), (12000, 20001)],
        [(20001, 30001)],
        [(10001, 11001)],
        tags=True,
    )


def test_start_partial_same(check_ranges, nft):
    """partial, touch start, merge, absolute"""
    nft.modifyRanges(1, 12000, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[1], 10001, 11001, {"from": accounts[2]})
    check_ranges(
        [(1, 11001)], [(11001, 12000), (12000, 20001)], [(20001, 30001)], [], tags=True
    )


def test_start_partial_same_abs(check_ranges, nft):
    """partial, touch start, merge"""
    nft.modifyRanges(8000, 12000, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[1], 10001, 11001, {"from": accounts[2]})
    check_ranges(
        [(1, 8000), (8000, 11001)],
        [(11001, 12000), (12000, 20001)],
        [(20001, 30001)],
        [],
        tags=True,
    )


def test_start_absolute(check_ranges, nft):
    """touch start, absolute"""
    nft.modifyRanges(1, 5000, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[4], 1, 100, {"from": accounts[1]})
    check_ranges(
        [(100, 5000), (5000, 10001)],
        [(10001, 20001)],
        [(20001, 30001)],
        [(1, 100)],
        tags=True,
    )


def test_stop_partial_different(check_ranges, nft):
    """partial, touch stop, no merge"""
    nft.modifyRanges(15000, 25000, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[4], 19000, 20001, {"from": accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 15000), (15000, 19000)],
        [(20001, 25000), (25000, 30001)],
        [(19000, 20001)],
        tags=True,
    )


def test_stop_partial_same_abs(check_ranges, nft):
    """partial, touch stop, merge, absolute"""
    nft.modifyRanges(15000, 30001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[3], 19000, 20001, {"from": accounts[2]})
    check_ranges(
        [(1, 10001)], [(10001, 15000), (15000, 19000)], [(19000, 30001)], [], tags=True
    )


def test_stop_partial_same(check_ranges, nft):
    """partial, touch stop, merge"""
    nft.modifyRanges(15000, 25000, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[3], 19000, 20001, {"from": accounts[2]})
    check_ranges(
        [(1, 10001)],
        [(10001, 15000), (15000, 19000)],
        [(19000, 25000), (25000, 30001)],
        [],
        tags=True,
    )


def test_stop_absolute(check_ranges, nft):
    """partial, touch stop, absolute"""
    nft.modifyRanges(29000, 30001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[4], 20001, 29000, {"from": accounts[3]})
    nft.transferRange(accounts[4], 29000, 30001, {"from": accounts[3]})
    check_ranges(
        [(1, 10001)], [(10001, 20001)], [], [(20001, 29000), (29000, 30001)], tags=True
    )


def test_whole_range_different(check_ranges, nft):
    """whole range, no merge"""
    nft.modifyRanges(1, 30001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[4], 10001, 20001, {"from": accounts[2]})
    check_ranges([(1, 10001)], [], [(20001, 30001)], [(10001, 20001)], tags=True)


def test_whole_range_same(check_ranges, nft):
    """whole range, merge both sides"""
    nft.modifyRanges(1, 30001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[3], 5000, 10001, {"from": accounts[1]})
    nft.transferRange(accounts[1], 25001, 30001, {"from": accounts[3]})
    nft.transferRange(accounts[3], 10001, 20001, {"from": accounts[2]})
    check_ranges([(1, 5000), (25001, 30001)], [], [(5000, 25001)], [], tags=True)


def test_whole_range_same_left(check_ranges, nft):
    """whole range, merge both sides, absolute left"""
    nft.modifyRanges(1, 30001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[1], 20001, 25000, {"from": accounts[3]})
    nft.transferRange(accounts[1], 10001, 20001, {"from": accounts[2]})
    check_ranges([(1, 25000)], [], [(25000, 30001)], [], tags=True)


def test_whole_range_same_right(check_ranges, nft):
    """whole range, merge both sides, absolute right"""
    nft.modifyRanges(1, 30001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[3], 5000, 10001, {"from": accounts[1]})
    nft.transferRange(accounts[3], 10001, 20001, {"from": accounts[2]})
    check_ranges([(1, 5000)], [], [(5000, 30001)], [], tags=True)


def test_whole_range_same_both(check_ranges, nft):
    """whole range, merge both sides, absolute both"""
    nft.modifyRanges(1, 30001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[3], 1, 10001, {"from": accounts[1]})
    nft.transferRange(accounts[3], 10001, 20001, {"from": accounts[2]})
    check_ranges([], [], [(1, 30001)], [], tags=True)


def test_whole_range_left_abs(check_ranges, nft):
    """whole range, merge left, absolute"""
    nft.modifyRanges(1, 20001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[1], 10001, 20001, {"from": accounts[2]})
    check_ranges([(1, 20001)], [], [(20001, 30001)], [], tags=True)


def test_whole_range_left(check_ranges, nft):
    """whole range, merge left"""
    nft.modifyRanges(1, 20001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[3], 1, 5001, {"from": accounts[1]})
    nft.transferRange(accounts[1], 10001, 20001, {"from": accounts[2]})
    check_ranges([(5001, 20001)], [], [(1, 5001), (20001, 30001)], [], tags=True)


def test_whole_range_right_abs(check_ranges, nft):
    """whole range, merge right, absolute"""
    nft.modifyRanges(10001, 30001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[3], 10001, 20001, {"from": accounts[2]})
    check_ranges([(1, 10001)], [], [(10001, 30001)], [], tags=True)


def test_whole_range_right(check_ranges, nft):
    """whole range, merge right"""
    nft.modifyRanges(10001, 30001, 0, "0x01", {"from": accounts[0]})
    nft.transferRange(accounts[1], 25001, 30001, {"from": accounts[3]})
    nft.transferRange(accounts[3], 10001, 20001, {"from": accounts[2]})
    check_ranges([(1, 10001), (25001, 30001)], [], [(10001, 25001)], [], tags=True)

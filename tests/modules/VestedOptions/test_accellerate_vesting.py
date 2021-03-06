#!/usr/bin/python3

from brownie import accounts


def test_accellerate_fully_unvested(options, id1, issueoptions, sleep, share):
    """fully unvested"""
    issueoptions(id1, 10)
    issueoptions(id1, 20)
    options.accellerateVesting(id1, {"from": accounts[0]})
    assert options.getOptions(id1) == (1000, 0, [(10, 1), (20, 1)])
    sleep(100)
    assert options.getOptions(id1) == (1000, 0, [(10, 1), (20, 1)])
    sleep(1)
    assert options.getOptions(id1) == (0, 0, [])


def test_accellerate_partially_unvested(options, id1, issueoptions, sleep):
    """partially vested"""
    issueoptions(id1, 10)
    issueoptions(id1, 20)
    sleep(2)
    options.accellerateVesting(id1, {"from": accounts[0]})
    assert options.getOptions(id1) == (1000, 0, [(10, 1), (20, 1)])
    assert options.getTotalOptionsAtPrice(10) == (500, 0)
    assert options.getTotalOptionsAtPrice(20) == (500, 0)
    assert options.totalOptions() == 1000
    sleep(98)
    assert options.getOptions(id1) == (1000, 0, [(10, 1), (20, 1)])
    sleep(1)
    assert options.getOptions(id1) == (0, 0, [])


def test_accellerate_already_vested(options, id1, issueoptions, sleep):
    """already vested"""
    issueoptions(id1, 10)
    issueoptions(id1, 20)
    sleep(7)
    options.accellerateVesting(id1, {"from": accounts[0]})
    assert options.getOptions(id1) == (1000, 0, [(10, 1), (20, 1)])
    assert options.getTotalOptionsAtPrice(10) == (500, 0)
    assert options.getTotalOptionsAtPrice(20) == (500, 0)
    assert options.totalOptions() == 1000
    sleep(93)
    assert options.getOptions(id1) == (1000, 0, [(10, 1), (20, 1)])
    sleep(1)
    assert options.getOptions(id1) == (0, 0, [])


def test_accellerate_multiple_expirations(options, id1, issueoptions, sleep):
    """accellerate multiple, different expirations"""
    issueoptions(id1, 10)
    sleep(2)
    issueoptions(id1, 10)
    sleep(2)
    issueoptions(id1, 10)
    sleep(1)
    options.accellerateVesting(id1, {"from": accounts[0]})
    assert options.getOptions(id1) == (1500, 0, [(10, 3)])
    assert options.getTotalOptionsAtPrice(10) == (1500, 0)
    assert options.totalOptions() == 1500


def test_accellerate_multiple_prices(options, id1, issueoptions, sleep):
    """accellerate multiple, different prices and expirations"""
    issueoptions(id1, 10)
    sleep(2)
    issueoptions(id1, 20)
    sleep(2)
    issueoptions(id1, 10)
    issueoptions(id1, 20)
    sleep(1)
    options.accellerateVesting(id1, {"from": accounts[0]})
    assert options.getOptions(id1) == (2000, 0, [(10, 2), (20, 2)])
    assert options.getTotalOptionsAtPrice(10) == (1000, 0)
    assert options.getTotalOptionsAtPrice(20) == (1000, 0)
    assert options.totalOptions() == 2000

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GameContract {
    struct Player {
        address ethAddress;
        uint score;
    }

    Player[] public players;
    address public owner;

    event GameStarted(Player[] players);
    event ScoreUpdated(address indexed ethAddress, uint newScore);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    constructor(address[] memory _players) {
        owner = msg.sender;
        for (uint i = 0; i < _players.length; i++) {
            players.push(Player(_players[i], 0));
        }
        emit GameStarted(players);
    }

    function updateScore(address _ethAddress, uint _newScore) public onlyOwner {
        for (uint i = 0; i < players.length; i++) {
            if (players[i].ethAddress == _ethAddress) {
                players[i].score = _newScore;
                emit ScoreUpdated(_ethAddress, _newScore);
            }
        }
    }

    function getPlayers() public view returns (Player[] memory) {
        return players;
    }
}

// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.26;

contract PlayerRegistration {
    struct Player {
        string name;
        address ethAddress;
        uint score;
    }

    mapping(address => Player) public players;
    address[] public playerAddresses;

    event PlayerRegistered(address indexed ethAddress, string name, uint score);

    function registerPlayer(string memory _name) public {
        address ethAddress = msg.sender;
        Player memory newPlayer = Player(_name, ethAddress, 0); // Initial score is 0
        players[ethAddress] = newPlayer;
        playerAddresses.push(ethAddress);

        emit PlayerRegistered(ethAddress, _name, 0);
    }

    function updateScore(address _ethAddress, uint _score) public {
        players[_ethAddress].score = _score;
    }

    function getPlayer(address _ethAddress) public view returns (string memory, address, uint) {
        Player memory player = players[_ethAddress];
        return (player.name, player.ethAddress, player.score);
    }
}
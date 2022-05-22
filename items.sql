-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 22, 2022 at 07:26 AM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tera`
--

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `category` varchar(20) NOT NULL,
  `icon` varchar(60) NOT NULL,
  `name` varchar(40) NOT NULL,
  `grade` int(1) NOT NULL,
  `level` int(2) NOT NULL,
  `classes` varchar(30) NOT NULL,
  `races` varchar(10) NOT NULL,
  `gender` varchar(1) NOT NULL DEFAULT '',
  `obtainable` int(1) NOT NULL,
  `tradable` int(1) NOT NULL,
  `dyeable` int(1) NOT NULL,
  `period` int(11) NOT NULL DEFAULT 0,
  `periodByWebAdmin` int(1) NOT NULL DEFAULT 0,
  `name_de` varchar(100) NOT NULL DEFAULT '',
  `name_en` varchar(100) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`id`, `category`, `icon`, `name`, `grade`, `level`, `classes`, `races`, `gender`, `obtainable`, `tradable`, `dyeable`, `period`, `periodByWebAdmin`, `name_de`, `name_en`) VALUES
(1, 'fabrication', 'icon_items/artisan_potion_tex', 'service_item_01', 1, 1, '', '', '', 1, 0, 0, 0, 0, 'Velika Mitternachts Öl', 'Velika Midnight Oil');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category` (`category`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

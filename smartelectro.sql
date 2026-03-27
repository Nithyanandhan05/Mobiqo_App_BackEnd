-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 27, 2026 at 04:20 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartelectro`
--

-- --------------------------------------------------------

--
-- Table structure for table `address`
--

CREATE TABLE `address` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `pincode` varchar(10) NOT NULL,
  `city` varchar(100) NOT NULL,
  `address_line` varchar(500) NOT NULL,
  `is_default` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `address`
--

INSERT INTO `address` (`id`, `user_id`, `full_name`, `mobile`, `pincode`, `city`, `address_line`, `is_default`) VALUES
(4, 1, 'Nithi', '9363441126', '631502', 'Kanchipuram', '30 Rajan Nagar Orikkai ', 0),
(6, 1, 'Nithyanandhan R', '9363441126', '631502', 'Chennai', 'Saveetha Hospital, Saveetha Nagar, Thandalam\n(SIMATS Engineering)', 1),
(7, 15, 'yg', '66', '66', 'yy', 'yy', 1),
(8, 15, 'tt', '22', '22', '4t', 'ft', 0);

-- --------------------------------------------------------

--
-- Table structure for table `ai_search_log`
--

CREATE TABLE `ai_search_log` (
  `id` int(11) NOT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `preferences` varchar(255) DEFAULT NULL,
  `recommended_product` varchar(255) DEFAULT NULL,
  `match_percent` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ai_search_log`
--

INSERT INTO `ai_search_log` (`id`, `user_id`, `preferences`, `recommended_product`, `match_percent`, `timestamp`) VALUES
(1, NULL, NULL, NULL, 95, '2026-02-26 12:44:24'),
(2, NULL, NULL, NULL, 95, '2026-02-26 15:03:08'),
(3, NULL, NULL, NULL, 95, '2026-02-27 12:50:39'),
(4, NULL, NULL, NULL, 95, '2026-03-02 13:55:19'),
(5, NULL, NULL, NULL, 95, '2026-03-02 13:55:43'),
(6, NULL, NULL, NULL, 95, '2026-03-03 08:54:33'),
(7, NULL, NULL, NULL, 95, '2026-03-03 10:50:02'),
(8, NULL, NULL, NULL, 95, '2026-03-03 12:29:46'),
(9, NULL, NULL, NULL, 95, '2026-03-03 12:30:23'),
(10, NULL, NULL, NULL, 95, '2026-03-03 12:49:26'),
(11, NULL, NULL, NULL, 95, '2026-03-03 12:54:53'),
(12, NULL, NULL, NULL, 95, '2026-03-03 13:06:48'),
(13, NULL, NULL, NULL, 95, '2026-03-03 13:41:19'),
(14, NULL, NULL, NULL, 95, '2026-03-03 14:01:09'),
(15, NULL, NULL, NULL, 95, '2026-03-03 14:02:14'),
(16, NULL, NULL, NULL, 95, '2026-03-04 08:20:53'),
(17, NULL, NULL, NULL, 95, '2026-03-04 08:33:50'),
(18, NULL, NULL, NULL, 95, '2026-03-04 08:53:28'),
(19, NULL, NULL, NULL, 95, '2026-03-04 09:17:00'),
(20, NULL, NULL, NULL, 95, '2026-03-04 09:33:11'),
(21, NULL, NULL, NULL, 95, '2026-03-04 09:40:32'),
(22, NULL, NULL, NULL, 95, '2026-03-04 09:42:12'),
(23, NULL, NULL, NULL, 95, '2026-03-04 09:55:35'),
(24, NULL, NULL, NULL, 95, '2026-03-04 13:01:16'),
(25, NULL, NULL, NULL, 95, '2026-03-04 14:29:07'),
(26, NULL, NULL, NULL, 95, '2026-03-05 09:41:45'),
(27, NULL, NULL, NULL, 95, '2026-03-05 14:02:32'),
(28, NULL, NULL, NULL, 95, '2026-03-05 21:55:55'),
(29, NULL, NULL, NULL, 95, '2026-03-06 08:47:01'),
(30, NULL, NULL, NULL, 95, '2026-03-06 13:27:03'),
(31, NULL, NULL, NULL, 95, '2026-03-06 13:45:13'),
(32, NULL, NULL, NULL, 95, '2026-03-06 15:57:49'),
(33, NULL, NULL, NULL, 95, '2026-03-06 21:12:30'),
(34, NULL, NULL, NULL, 95, '2026-03-08 11:39:57'),
(35, NULL, NULL, NULL, 95, '2026-03-08 15:20:51'),
(36, NULL, NULL, NULL, 95, '2026-03-09 08:48:26'),
(37, NULL, NULL, NULL, 95, '2026-03-09 08:54:38'),
(38, NULL, NULL, NULL, 95, '2026-03-09 14:52:18'),
(39, NULL, NULL, NULL, 95, '2026-03-10 09:23:49'),
(40, NULL, NULL, NULL, 95, '2026-03-11 10:44:26'),
(41, NULL, NULL, NULL, 95, '2026-03-11 13:27:41'),
(42, NULL, NULL, NULL, 95, '2026-03-11 14:14:22'),
(43, NULL, NULL, NULL, 95, '2026-03-14 09:46:42'),
(44, NULL, NULL, NULL, 95, '2026-03-16 08:42:23'),
(45, NULL, NULL, NULL, 95, '2026-03-16 08:50:07'),
(46, NULL, NULL, NULL, 95, '2026-03-16 08:59:12'),
(47, NULL, NULL, NULL, 95, '2026-03-17 08:36:00'),
(48, NULL, NULL, NULL, 95, '2026-03-17 10:45:36'),
(49, NULL, NULL, NULL, 95, '2026-03-17 10:51:37'),
(50, NULL, NULL, NULL, 95, '2026-03-17 12:22:19'),
(51, NULL, NULL, NULL, 95, '2026-03-17 12:25:01'),
(52, NULL, NULL, NULL, 95, '2026-03-17 12:30:26'),
(53, NULL, NULL, NULL, 95, '2026-03-17 12:57:00'),
(54, NULL, NULL, NULL, 95, '2026-03-17 13:16:04'),
(55, NULL, NULL, NULL, 95, '2026-03-17 13:52:30'),
(56, NULL, NULL, NULL, 95, '2026-03-17 13:56:07'),
(57, NULL, NULL, NULL, 95, '2026-03-17 14:01:16'),
(58, NULL, NULL, NULL, 95, '2026-03-17 14:04:36'),
(59, NULL, NULL, NULL, 95, '2026-03-17 14:11:54'),
(60, NULL, NULL, NULL, 95, '2026-03-17 14:12:11'),
(61, NULL, NULL, NULL, 95, '2026-03-17 14:12:56'),
(62, NULL, NULL, NULL, 95, '2026-03-17 14:22:43'),
(63, NULL, NULL, NULL, 95, '2026-03-17 14:27:22'),
(64, NULL, NULL, NULL, 95, '2026-03-17 14:32:41'),
(65, NULL, NULL, NULL, 95, '2026-03-17 14:37:33'),
(66, NULL, NULL, NULL, 95, '2026-03-19 07:59:39'),
(67, NULL, NULL, NULL, 95, '2026-03-19 12:09:21'),
(68, NULL, NULL, NULL, 95, '2026-03-23 08:44:22'),
(69, NULL, NULL, NULL, 95, '2026-03-23 09:11:41'),
(70, NULL, NULL, NULL, 95, '2026-03-23 09:20:41'),
(71, NULL, NULL, NULL, 95, '2026-03-23 09:21:34'),
(72, NULL, NULL, NULL, 95, '2026-03-23 09:22:01'),
(73, NULL, NULL, NULL, 95, '2026-03-23 09:22:25'),
(74, NULL, NULL, NULL, 95, '2026-03-23 09:22:59'),
(75, NULL, NULL, NULL, 95, '2026-03-23 09:41:34'),
(76, NULL, NULL, NULL, 95, '2026-03-23 10:19:17'),
(77, NULL, NULL, NULL, 95, '2026-03-23 10:21:15'),
(78, NULL, NULL, NULL, 95, '2026-03-23 12:20:57'),
(79, NULL, NULL, NULL, 95, '2026-03-23 12:21:14'),
(80, NULL, NULL, NULL, 95, '2026-03-23 12:48:15'),
(81, NULL, NULL, NULL, 95, '2026-03-23 12:49:09'),
(82, NULL, NULL, NULL, 95, '2026-03-23 12:58:14'),
(83, NULL, NULL, NULL, 95, '2026-03-23 12:58:55'),
(84, NULL, NULL, NULL, 95, '2026-03-23 12:59:32'),
(85, NULL, NULL, NULL, 95, '2026-03-23 13:11:54'),
(86, NULL, NULL, NULL, 95, '2026-03-23 13:23:23'),
(87, NULL, NULL, NULL, 95, '2026-03-23 13:23:44'),
(88, NULL, NULL, NULL, 95, '2026-03-23 13:24:02'),
(89, NULL, NULL, NULL, 95, '2026-03-23 13:28:54'),
(90, NULL, NULL, NULL, 95, '2026-03-23 13:32:27'),
(91, NULL, NULL, NULL, 95, '2026-03-23 13:37:34'),
(92, NULL, NULL, NULL, 95, '2026-03-23 13:38:02'),
(93, NULL, NULL, NULL, 95, '2026-03-23 13:38:43'),
(94, NULL, NULL, NULL, 95, '2026-03-24 08:20:53'),
(95, NULL, NULL, NULL, 95, '2026-03-24 08:21:22'),
(96, NULL, NULL, NULL, 95, '2026-03-24 08:21:41'),
(97, NULL, NULL, NULL, 95, '2026-03-24 08:22:05'),
(98, NULL, NULL, NULL, 95, '2026-03-24 08:22:53'),
(99, NULL, NULL, NULL, 95, '2026-03-24 13:25:36'),
(100, NULL, NULL, NULL, 95, '2026-03-24 14:34:48'),
(101, NULL, NULL, NULL, 95, '2026-03-25 20:29:38');

-- --------------------------------------------------------

--
-- Table structure for table `ai_setting`
--

CREATE TABLE `ai_setting` (
  `id` int(11) NOT NULL,
  `is_enabled` tinyint(1) DEFAULT NULL,
  `gaming_weight` int(11) DEFAULT NULL,
  `camera_weight` int(11) DEFAULT NULL,
  `battery_weight` int(11) DEFAULT NULL,
  `budget_weight` int(11) DEFAULT NULL,
  `engine_mode` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ai_setting`
--

INSERT INTO `ai_setting` (`id`, `is_enabled`, `gaming_weight`, `camera_weight`, `battery_weight`, `budget_weight`, `engine_mode`) VALUES
(1, 1, 24, 26, 24, 72, 'Performance Mode');

-- --------------------------------------------------------

--
-- Table structure for table `compare_device_cache`
--

CREATE TABLE `compare_device_cache` (
  `id` int(11) NOT NULL,
  `search_query` varchar(100) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `spec_score` varchar(20) DEFAULT NULL,
  `release_date` varchar(50) DEFAULT NULL,
  `processor` varchar(100) DEFAULT NULL,
  `cores` varchar(100) DEFAULT NULL,
  `ram` varchar(50) DEFAULT NULL,
  `disp_type` varchar(100) DEFAULT NULL,
  `disp_res` varchar(100) DEFAULT NULL,
  `disp_refresh` varchar(50) DEFAULT NULL,
  `disp_size` varchar(50) DEFAULT NULL,
  `cam_main` varchar(100) DEFAULT NULL,
  `cam_sec` varchar(100) DEFAULT NULL,
  `cam_tert` varchar(100) DEFAULT NULL,
  `cam_front` varchar(100) DEFAULT NULL,
  `bat_capacity` varchar(50) DEFAULT NULL,
  `bat_charging` varchar(50) DEFAULT NULL,
  `storage_internal` varchar(50) DEFAULT NULL,
  `storage_type` varchar(50) DEFAULT NULL,
  `pros` text DEFAULT NULL,
  `cons` text DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `antutu_score` varchar(50) DEFAULT NULL,
  `battery_life` varchar(50) DEFAULT NULL,
  `expert_score` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `compare_device_cache`
--

INSERT INTO `compare_device_cache` (`id`, `search_query`, `name`, `price`, `spec_score`, `release_date`, `processor`, `cores`, `ram`, `disp_type`, `disp_res`, `disp_refresh`, `disp_size`, `cam_main`, `cam_sec`, `cam_tert`, `cam_front`, `bat_capacity`, `bat_charging`, `storage_internal`, `storage_type`, `pros`, `cons`, `image_url`, `antutu_score`, `battery_life`, `expert_score`) VALUES
(1, 'samsung s23', 'Samsung Galaxy S23', '₹74,999', '92/100', 'February 2023', 'Qualcomm Snapdragon 8 Gen 2 for Galaxy', 'Octa-Core', '8 GB', 'Dynamic AMOLED 2X', '2340 x 1080 pixels (FHD+)', '120 Hz adaptive', '6.1 inches', '50 MP (Wide-angle)', '12 MP (Ultra-wide)', '10 MP (Telephoto)', '12 MP', '3900 mAh', '25W Fast Charging', '128 GB, 256 GB, 512 GB', 'UFS 4.0 (UFS 3.1 for 128GB variant)', '[\"Compact and premium design for one-handed use.\", \"Excellent performance powered by Snapdragon 8 Gen 2 for Galaxy.\", \"Versatile and capable camera system with good low-light performance.\"]', '[\"Slower charging speeds compared to some competitors.\", \"Minor upgrades over its predecessor, the Galaxy S22.\", \"No Ultra-Wideband (UWB) support.\"]', 'https://rukminim2.flixcart.com/image/480/640/xif0q/mobile/y/8/i/-original-imah4zp7fgtezhsz.jpeg?q=90', '1,507,884 (v10)', '11h 50m (PC Mark)', '4.5/5'),
(2, 'samsung s24', 'Samsung Galaxy S24 5G', '₹74,999', '92/100', 'January 2024', 'Exynos 2400', 'Deca-core (1x3.2GHz Cortex-X4 & 2x2.9GHz Cortex-A720 & 3x2.6GHz Cortex-A720 & 4x1.95GHz Cortex-A520)', '8GB', 'Dynamic AMOLED 2X', '2340 x 1080 pixels (FHD+)', '120Hz (variable, 1Hz or 24Hz to 120Hz)', '6.2-inch (15.75 cm)', '50 MP (wide, f/1.8, OIS, Dual Pixel PDAF)', '12 MP (ultrawide, f/2.2)', '10 MP (telephoto, 3x optical zoom, f/2.4, OIS, PDAF)', '12 MP (f/2.2)', '4000 mAh', '25W wired, 15W wireless, 4.5W reverse wireless', '128GB, 256GB', 'UFS 3.1 (128GB), UFS 4.0 (256GB and above)', '[\"Stunning Dynamic AMOLED 2X display with 120Hz refresh rate.\", \"Powerful Exynos 2400 processor for smooth performance.\", \"Advanced camera system with AI enhancements.\"]', '[\"Slower 25W wired charging compared to some competitors.\", \"No expandable storage via microSD card slot.\", \"Exynos processor in India (some users prefer Snapdragon).\"]', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRA2EDNyE14d55TWWLQDRVI2HD9TeWBvi99b0f8vVBtolJey0fTiJpN8fN6hSFAtVsQsXCwUUJTNCwq2hbczwo2nRhw9IXPeAqvXcblg-73vNNxbQ25JqtDL4tQRQ-JUF41z9uu4Q&usqp=CAc', '1,935,000 (v11)', 'Up to 1.5 days (34 hours) or 13-15 hours video pla', '4.0/5'),
(3, 'samsung galaxy s25 ultra', 'Samsung Galaxy S25 Ultra', '₹109,490', '94/100', 'February 2025', 'Qualcomm Snapdragon 8 Elite for Galaxy', 'Octa-core', '12GB', 'Dynamic AMOLED 2X', 'QHD+ (1400x3120 pixels)', '120Hz adaptive', '6.9-inch', '200MP Wide Angle', '50MP Ultra-Wide Angle', '50MP Telephoto (5x Optical Zoom)', '12MP', '5000mAh', '45W Wired, 25W Wireless', '256GB', 'UFS 4.0', '[\"Exceptional performance powered by the Snapdragon 8 Elite for Galaxy processor.\", \"Highly versatile and upgraded quad-camera system, including a 200MP main sensor and improved 50MP ultrawide.\", \"Immersive 6.9-inch QHD+ Dynamic AMOLED 2X display with a smooth 120Hz adaptive refresh rate.\"]', '[\"Premium price point may be a significant barrier for some users.\", \"Charging speeds, while fast, are not class-leading compared to some competitors in the flagship segment.\", \"Large form factor and weight might be cumbersome for one-handed use or users preferring smaller devices.\"]', 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?q=80&w=600', '2,400,000+', 'Excellent, up to 2 days moderate use', '4.7/5'),
(4, 'samsung galaxy s26 ultra 5g', 'Samsung Galaxy S26 Ultra 5G', '₹1,39,999', '95/100', 'February 2026', 'Qualcomm Snapdragon 8 Elite Gen 5 for Galaxy', 'Octa-core (2x 4.74 GHz Oryon V3 Phoenix L + 6x 3.63 GHz Oryon V3 Phoenix M)', '12GB, 16GB LPDDR5X', 'Dynamic AMOLED 2X', '3120 x 1440 pixels (QHD+)', '1-120Hz Adaptive', '6.9 inches', '200MP Wide (f/1.4, OIS AF)', '50MP Ultra-Wide (f/1.9)', '50MP Telephoto (5x Optical Zoom, f/2.9) + 10MP Telephoto (3x Optical Zoom, f/2.4)', '', '5000 mAh', '60W Wired (Super Fast Charging 3.0), 25W Wireless', '256GB, 512GB, 1TB', 'UFS 4.0', '[\"Industry-leading camera system with enhanced low-light performance.\", \"Cutting-edge Snapdragon 8 Elite Gen 5 for Galaxy processor for unrivaled performance.\", \"Innovative Privacy Display and immersive QHD+ Dynamic AMOLED 2X screen.\"]', '[\"Exorbitant price point makes it inaccessible for many users.\", \"Large and heavy design, potentially bulky for single-handed use.\", \"Wired charging speed, while improved, is not class-leading compared to some competitors.\"]', 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?q=80&w=600', '3,720,219 (v11)', 'Excellent', '4.8/5'),
(5, 'oneplus 12', 'OnePlus 12', '₹69,999', 'N/A', 'January 2024', 'Qualcomm Snapdragon 8 Gen 3', 'Octa-core (1x3.3 GHz Cortex-X4 & 5x3.2 GHz Cortex-A720 & 2x2.3 GHz Cortex-A520)', '12GB, 16GB LPDDR5X', 'LTPO AMOLED, 1B colors, Dolby Vision, HDR10+', '1440 x 3168 pixels (2K)', '1Hz-120Hz adaptive', '6.82 inches', '50 MP, f/1.6, 23mm (wide), 1/1.43\", 1.12µm, multi-directional PDAF, OIS (Sony LYT-808)', '48 MP, f/2.2, 14mm, 114˚ (ultrawide), 1/2.0\", 0.8µm, PDAF (Sony IMX 581)', '64 MP, f/2.6, 70mm (periscope telephoto), 1/2.0\", 0.7µm, PDAF, OIS, 3x optical zoom (OmniVision OV64', '32 MP', '5400 mAh', '100W SUPERVOOC wired, 50W AIRVOOC wireless', '256GB, 512GB', 'UFS 4.0', '[\"Excellent battery life and ultra-fast charging (100W wired, 50W wireless).\", \"Stunning 2K 120Hz ProXDR AMOLED display with high peak brightness.\", \"Top-tier performance powered by the Qualcomm Snapdragon 8 Gen 3 SoC.\"]', '[\"Shorter software update commitment compared to some rivals like Samsung and Google.\", \"Camera performance, especially the ultrawide and in low light, can lag behind top competitors, and lacks advanced AI photo features.\", \"IP65 rating for dust and water resistance, which is not the flagship standard IP68.\"]', 'https://m.media-amazon.com/images/I/71xMs88FYbL._AC_SL1500_.jpg', '2,333,033', 'Offers excellent battery life, lasting 52-55 hours', '4.0/5'),
(6, 'oneplus 13', 'OnePlus 13', '₹69,999', '92/100', 'January 2025', 'Qualcomm Snapdragon 8 Elite', 'Octa Core', 'Up to 24GB', 'LTPO AMOLED', '1440 x 3168 pixels', '1-120Hz adaptive', '6.82 inches', '50MP Sony LYT-808, f/1.6, OIS', '50MP Ultrawide, f/2.0, 15mm, 120˚', '50MP Periscope Telephoto, f/2.6, 73mm, 3x optical zoom', '32MP, f/2.45, 21mm', '6000mAh', '100W wired, 50W wireless', 'Up to 1TB', 'UFS 4.0', '[\"Exceptional battery life with 6000mAh capacity and rapid 100W wired/50W wireless charging.\", \"Cutting-edge performance powered by the Qualcomm Snapdragon 8 Elite processor and up to 24GB of RAM.\", \"Versatile and high-quality triple 50MP Hasselblad-tuned camera system with 3x optical zoom and 4K Dolby Vision support.\"]', '[\"The curved display may lead to accidental touches and challenges with screen protector application.\", \"While excellent, the camera system exhibits occasional white balance inconsistencies and a 3x telephoto zoom that some competitors exceed.\", \"Reports suggest the device may experience some heating during prolonged heavy usage.\"]', 'https://sm.pcmag.com/t/pcmag_me/review/o/oneplus-13/oneplus-13_kd8t.1200.jpg', '2,300,000+', 'Excellent (Over 24 hours of mixed use)', '4.5/5'),
(7, 's25 ultra', 'Samsung Galaxy S25 Ultra', '₹129,999', '92/100', 'February 2025', 'Snapdragon 8 Elite for Galaxy', 'Octa-core', '12GB', 'Dynamic LTPO AMOLED 2X', '3120 x 1440 (QHD+)', '120Hz', '6.9 inches', '200MP Wide Angle', '50MP Ultra-Wide Angle', '50MP Telephoto (5x Optical Zoom)', '12MP', '5000mAh', '45W Wired, Wireless Charging', '256GB', 'UFS 4.0', '[\"Powerful Snapdragon 8 Elite for Galaxy processor for top-tier performance.\", \"Versatile quad-camera system with a 200MP main sensor and improved 50MP ultrawide.\", \"Stunning 6.9-inch Dynamic LTPO AMOLED 2X display with a smooth 120Hz refresh rate.\"]', '[\"S Pen loses Bluetooth functionality, removing remote control features.\", \"Offers iterative upgrades compared to its predecessor, the S24 Ultra.\", \"Battery capacity remains unchanged from the previous generation at 5000mAh.\"]', 'https://cdn.dummyjson.com/product-images/3/thumbnail.jpg', '3,135,223 (v11)', '13 hours 51 minutes (PCMark)', '4.5/5'),
(8, 's26 ultra', 'Samsung Galaxy S26 Ultra', '₹1,39,999', '92/100', 'February 2026', 'Snapdragon 8 Elite Gen 5 for Galaxy', 'Octa-Core', '12GB, 16GB', 'Dynamic AMOLED 2X', '3120x1440 (QHD+)', '1-120Hz adaptive', '6.9-inch', '200MP Wide (F1.4)', '50MP Ultra-Wide (F1.9)', '50MP Telephoto (5x Optical Zoom, F2.9) + 10MP Telephoto (3x Optical Zoom, F2.4)', '12MP (F2.2)', '5,000 mAh', '60W wired, 25W wireless', '256GB, 512GB, 1TB', 'UFS 4.0', '[\"Powered by the latest and most powerful Snapdragon 8 Elite Gen 5 for Galaxy processor, offering significant performance gains.\", \"Features a versatile quad-camera system with a 200MP main sensor, enhanced Nightography, and advanced zoom capabilities.\", \"Boasts a large 6.9-inch QHD+ Dynamic AMOLED 2X display with an adaptive 1-120Hz refresh rate for immersive visuals.\"]', '[\"Comes with a high starting price in India, with higher storage variants being significantly more expensive.\", \"Lacks expandable storage via a microSD card slot, limiting storage flexibility beyond internal options.\", \"The charging adapter is not included in the box, requiring a separate purchase for fast charging.\"]', 'https://cdn.dummyjson.com/product-images/3/thumbnail.jpg', '2,600,000+', 'Up to 2 days of mixed usage', '4.7/5'),
(9, 'smartphone samsung galaxy s24 ultra', 'Samsung Galaxy S24 Ultra', '₹1,29,999', '92/100', 'January 2024', 'Qualcomm Snapdragon 8 Gen 3 for Galaxy', '8-core (1x 3.39 GHz Cortex-X4, 3x 3.15 GHz Cortex-A720, 2x 2.96 GHz Cortex-A720, 2x 2.27 GHz Cortex-', '12GB', 'Dynamic LTPO AMOLED 2X', '1440 x 3120 pixels', '120Hz', '6.8 inches', '200 MP, f/1.7 (wide), OIS', '50 MP, f/3.4 (periscope telephoto), 5x optical zoom, OIS', '10 MP, f/2.4 (telephoto), 3x optical zoom, OIS', '12 MP, f/2.2 (wide), Dual Pixel PDAF', '5000 mAh', '45W wired, 15W wireless, 4.5W reverse wireless', '256GB', 'UFS 4.0', '[\"Exceptional camera system with versatile zoom capabilities.\", \"Powerful Qualcomm Snapdragon 8 Gen 3 for Galaxy processor delivers top-tier performance.\", \"Guaranteed 7 years of Android OS and security updates.\"]', '[\"Wired charging speed (45W) is slower compared to some competitors.\", \"Lacks a microSD card slot for expandable storage.\", \"High launch price in the Indian market.\"]', 'https://assets.superhivemarket.com/store/product/200518/image/f9862d0fc9fe8edf268427df419eb579.png', '1,952,680', 'Excellent, easily lasting over a day with heavy us', '4.4/5'),
(10, 'samsung s 26 ultra', 'Samsung Galaxy S26 Ultra', '₹1,39,999', '92/100', 'February 2026', 'Snapdragon 8 Elite Gen 5 for Galaxy', 'Octa-core', '16GB', 'Dynamic AMOLED 2X LTPO', '3120 x 1440 (QHD+)', '1-120Hz Adaptive', '6.9-inch', '200MP Wide (F1.4)', '50MP Ultra-Wide (F1.9)', '50MP Telephoto (5x Optical / 10x Optical Quality Zoom, F2.9)', '12MP (F2.2)', '5,000 mAh', '60W Wired, 25W Wireless', '256GB, 512GB, 1TB', 'UFS 4.0', '[\"Cutting-edge Snapdragon 8 Elite Gen 5 processor for unparalleled performance.\", \"Advanced quad-camera system with a 200MP main sensor and enhanced AI features.\", \"Stunning 6.9-inch QHD+ Dynamic AMOLED 2X display with 1-120Hz adaptive refresh rate.\"]', '[\"Premium price point, making it less accessible.\", \"No expandable storage via microSD card.\", \"Charger not included in the box.\"]', 'https://mobileinto.com/images/largepic/large_samsung-galaxy-s26-ultra_2.jpg', 'N/A', 'Excellent all-day battery life', 'N/A'),
(11, 'oneplus nord ce3 5g', 'OnePlus Nord CE3 5G', '₹26,999', '80/100', 'August 2023', 'Qualcomm Snapdragon 782G', 'Octa-core (1x 2.7 GHz Cortex-A78 + 3x 2.4 GHz Cortex-A78 + 4x 1.8 GHz Cortex-A55)', '8GB, 12GB LPDDR4X', 'Fluid AMOLED', '2412 x 1080 pixels (FHD+), 394 ppi', '120Hz adaptive', '6.7 inches', '50MP Sony IMX890 (f/1.8, OIS)', '8MP Ultra-wide (f/2.2, 112° FOV)', '2MP Macro (f/2.4)', '16MP (f/2.4)', '5000 mAh', '80W SuperVOOC', '128GB, 256GB', 'UFS 3.1', '[\"Powerful Snapdragon 782G processor for seamless performance.\", \"Flagship-grade 50MP Sony IMX890 primary camera with OIS.\", \"Rapid 80W SuperVOOC fast charging and good battery life.\"]', '[\"Lacks the signature Alert Slider.\", \"Plastic build for the back and sides.\", \"No 3.5mm headphone jack.\"]', 'https://wsrv.nl/?url=https%3A//rukminim2.flixcart.com/image/416/416/xif0q/mobile/l/7/k/-original-imagtxvur9yrxvru.jpeg%3Fq%3D70&w=600&output=webp', '635,774 (v10)', 'Excellent, up to 2 days on normal usage', 'N/A'),
(12, 'iphone 16 pro', 'iPhone 16 Pro', '₹1,19,900', '87/100', 'September 2024', 'Apple A18 Pro', '6-core CPU (2 performance, 4 efficiency), 6-core GPU, 16-core Neural Engine', '8GB', 'Super Retina XDR OLED with ProMotion', '2622x1206 pixels', '120 Hz adaptive', '6.3 inches', '48MP (f/1.78, 24mm, second-generation sensor-shift OIS)', '48MP Ultra Wide (f/2.2, 13mm)', '12MP Telephoto (5x optical zoom)', '12MP (f/1.9, autofocus)', '3582 mAh', '30W wired, 22W MagSafe wireless', '128GB, 256GB, 512GB, 1TB', 'NVMe', '[\"Stunning and brighter Super Retina XDR OLED display with ProMotion and thinner bezels.\", \"Exceptional performance powered by the Apple A18 Pro chip and 8GB RAM, with advanced AI capabilities.\", \"Highly versatile and upgraded camera system, including a 48MP Ultra Wide lens and 5x optical zoom on both Pro models.\"]', '[\"Battery life, while improved, is still shorter compared to the larger iPhone 16 Pro Max.\", \"The base storage option remains at 128GB, which may be insufficient for some users.\", \"High price point, making it a significant investment.\"]', 'https://wsrv.nl/?url=https%3A//static.digit.in/iPhone-16-Pro-.png&w=600&output=webp', '1,950,000+', 'All-day usage, up to 27 hours video playback', '4.0/5'),
(13, 'iphone pro 13 pro', 'iPhone 13 Pro', '₹119,900', '92/100', 'September 2021', 'Apple A15 Bionic', '6-core CPU (2 performance, 4 efficiency), 5-core GPU, 16-core Neural Engine', '6GB', 'Super Retina XDR OLED with ProMotion', '2532 x 1170 pixels at 460 ppi', '10-120Hz adaptive ProMotion', '6.1-inch', '12MP Wide (f/1.5, sensor-shift OIS)', '12MP Telephoto (f/2.8, 3x optical zoom, OIS)', '12MP Ultra Wide (f/1.8, 120˚ FoV, PDAF)', '12MP TrueDepth (f/2.2)', '3095 mAh', 'Fast-charge (up to 50% in ~30 mins with 20W adapte', '128GB, 256GB, 512GB, 1TB', 'NVMe', '[\"Exceptional camera system with 3x optical zoom and macro capabilities.\", \"Stunning 120Hz ProMotion Super Retina XDR display.\", \"Powerful A15 Bionic chip for top-tier performance.\"]', '[\"Still uses Lightning port, not USB-C.\", \"Charger not included in the box.\", \"Relatively heavy for its size.\"]', 'https://wsrv.nl/?url=https%3A//m.media-amazon.com/images/I/61nEaHtArzL._AC_UL960_QL65_.jpg&w=600&output=webp', '839,675 (v9)', 'Up to 22 hours video playback; easily lasts a full', '4.6/5'),
(14, 'samsung galaxy s24 ultra 5g ai', 'Samsung Galaxy S24 Ultra 5G AI', '₹129,999', '92/100', 'January 2024', 'Qualcomm Snapdragon 8 Gen 3 for Galaxy', '1x 3.4 GHz Cortex-X4, 3x 3.15 GHz Cortex-A720, 2x 2.96 GHz Cortex-A520, 2x 2.27 GHz Cortex-A520 (Oct', '12GB', 'Dynamic LTPO AMOLED 2X', '1440 x 3120 pixels (QHD+)', '120Hz adaptive (1-120Hz)', '6.8-inch', '200MP Wide Angle (OIS, F1.7)', '12MP Ultra-Wide Angle (F2.2)', '50MP Telephoto (5x Optical Zoom, OIS, F3.4) + 10MP Telephoto (3x Optical Zoom, OIS, F2.4)', '12MP (F2.2)', '5000mAh', '45W Wired Fast Charging, 15W Wireless Charging (Fa', '256GB (also available in 512GB, 1TB)', 'UFS 4.0', '[\"Fantastic Dynamic AMOLED 2X display with high brightness, QHD+ resolution, and anti-glare coating.\", \"Versatile and powerful quad-camera system with a 200MP main sensor and excellent 3x and 5x optical zoom capabilities.\", \"Top-tier performance powered by the Snapdragon 8 Gen 3 for Galaxy processor, coupled with a long software support commitment of seven years.\"]', '[\"High price point, making it one of the most expensive smartphones on the market.\", \"Large and heavy form factor, which might be cumbersome for some users.\", \"AI features may require a paid subscription after 2025, and might not be a primary reason for purchase for all users.\"]', 'https://wsrv.nl/?url=https%3A//fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s24-ultra-5g-sm-s928-0.jpg&w=600&output=webp', '2,026,663 (v10)', 'Excellent (e.g., 14+ hours of screen-on time, PCMa', '4.5/5'),
(15, 'samsung s26 ultra specs', 'Samsung Galaxy S26 Ultra', '₹129,999', '92/100', 'March 2026', 'Qualcomm Snapdragon 8 Elite Gen 5 for Galaxy', 'Octa-core', '12GB, 16GB LPDDR5X', 'Dynamic AMOLED 2X LTPO', '3120 x 1440 (QHD+)', '1-120Hz Adaptive', '6.9 inches', '200MP Wide Angle (f/1.7)', '50MP Periscope Telephoto (5x Optical Zoom)', '10MP Telephoto (3x Optical Zoom)', '12MP', '5000 mAh', '60W Wired, 15W Wireless', '256GB, 512GB, 1TB', 'UFS 4.0', '[\"Powerful Snapdragon 8 Elite Gen 5 for Galaxy processor with significant performance improvements.\", \"Advanced Quad Camera system with a 200MP main sensor and improved telephoto capabilities.\", \"Faster 60W wired charging and a durable QHD+ Dynamic AMOLED 2X display.\"]', '[\"Battery capacity remains unchanged from previous generations.\", \"Charger is not included in the box.\", \"Display core specifications are largely unchanged from its predecessor.\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F71HXOEh%2BU1L.jpg&f=1&nofb=1', '2,500,000+', 'Excellent, with all-day usage', '4.5/5'),
(17, 's23 ultra', 'Samsung Galaxy S23 Ultra', '₹1,24,999', '92/100', 'February 2023', 'Qualcomm Snapdragon 8 Gen 2 for Galaxy', 'Octa-Core (1x 3.36 GHz Cortex-X3, 2x 2.8 GHz Cortex-A715, 2x 2.8 GHz Cortex-A710, 3x 2.0 GHz Cortex-', '12 GB', 'Dynamic AMOLED 2X', '3088 x 1440 pixels (QHD+)', '120 Hz (Adaptive 1-120Hz)', '6.8 inches', '200 MP Wide Angle (f/1.7, OIS)', '12 MP Ultra-Wide Angle (f/2.2, 120˚)', '10 MP Telephoto (3x Optical Zoom, f/2.4, OIS)', '12 MP Wide Angle (f/2.2)', '5000 mAh', '45W Fast Charging, 15W Wireless Charging', '256 GB', 'UFS 4.0', '[\"Supremely versatile camera system with a 200MP main sensor and excellent zoom capabilities.\", \"Features a fantastic Dynamic AMOLED 2X display with QHD+ resolution, 120Hz adaptive refresh rate, and 1750 nits peak brightness.\", \"Delivers powerful performance thanks to the custom Qualcomm Snapdragon 8 Gen 2 for Galaxy processor, LPDDR5X RAM, and UFS 4.0 storage.\"]', '[\"The camera\'s auto mode can sometimes apply heavy-handed processing to images.\", \"The design is very similar to its predecessor, the Samsung Galaxy S22 Ultra.\", \"Its large size and weight may make it too big for some users to comfortably handle.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwby61R2RqNtMBJtMgzIn_6HG4MYFx-0dCC9ifjCzv0tV-XX73dbIqQTE2jYk&s', '1,226,598', '13h 52m', '4.25/5'),
(18, 'iphone 15 pro max', 'iPhone 15 Pro Max', '₹159,900', '92/100', 'September 2023', 'Apple A17 Pro', '6-core CPU, 6-core GPU', '8GB', 'Super Retina XDR OLED', '2796 x 1290 pixels at 460 ppi', 'Up to 120Hz (ProMotion)', '6.7-inch', '48MP, f/1.78, second-generation sensor-shift OIS', '12MP Ultra Wide, f/2.2, 120° FOV', '12MP 5x Telephoto, f/2.8, 3D sensor-shift OIS (120mm equivalent)', '12MP, f/1.9, autofocus with Focus Pixels', '4422 mAh', '20W wired (USB-C), 50% in 30 minutes', '256GB, 512GB, 1TB', 'NVMe', '[\"Exceptional performance with A17 Pro chip\", \"Versatile and high-quality camera system, including 5x optical zoom\", \"Excellent all-day battery life\"]', '[\"High price point in India\", \"Relatively slow wired charging speeds compared to competitors\", \"Battery life, while excellent, shows no significant improvement over its predecessor\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQNwAFQHqnB2PPLzqzuZSSbJwb2H94sjH_aQuqlbgCXos4XcJmIVB15nmo7w&s', '1,641,883 (v10)', 'Excellent, easily lasts a full day, up to 2 days w', '4.5/5'),
(19, 'samsung galaxy s24 5g ai', 'Samsung Galaxy S24 5G', '₹40,999', '92/100', 'January 2024', 'Samsung Exynos 2400', 'Octa-core', '8GB', 'Dynamic AMOLED 2X', '1080 x 2340 pixels (FHD+)', 'Adaptive 120Hz', '6.2 inches', '50MP', '12MP (Ultra-wide)', '10MP (Telephoto, 3x optical zoom)', '12MP', '4000mAh', '25W wired, 15W wireless, 4.5W reverse wireless', '128GB', 'UFS 3.1', '[\"Excellent battery life for a compact phone.\", \"Stunning and bright Dynamic AMOLED 2X display.\", \"Powerful performance and useful Galaxy AI features.\"]', '[\"No significant camera improvements over its predecessor.\", \"Slower charging speeds compared to many competitors.\", \"Battery drain on standby can be faster than desired.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN7pg9m9N8EaFd0ynyXZ7k0ccv3ZsrUcmsVM0ukmcwhSIJf8xVK6SogNWkGJ0&s', '2,011,752 (v11)', '13 hours and 28 minutes', '4.5/5'),
(20, 'smartphone samsung galaxy s23 ultra', 'Samsung Galaxy S23 Ultra', '₹76,999', 'N/A', 'February 2023', 'Qualcomm Snapdragon 8 Gen 2 for Galaxy', 'Octa-Core (1x 3.36 GHz Cortex-X3, 2x 2.8 GHz Cortex-A715, 2x 2.8 GHz Cortex-A710, 3x 2.0 GHz Cortex-', '12 GB', 'Dynamic AMOLED 2X', '3088 x 1440 (Edge Quad HD+)', 'Adaptive 1~120Hz', '6.8 inches (17.27 cm)', '200 MP Wide Angle Primary Camera (f/1.7)', '12 MP Ultra-Wide Angle Camera (f/2.2)', '10 MP Telephoto (3x Optical Zoom, f/2.4) & 10 MP Telephoto (10x Optical Zoom, f/4.9)', '12 MP', '5000 mAh', '45W Fast Charging', '256 GB', 'UFS 4.0', '[\"Brilliant and vibrant Dynamic AMOLED 2X display.\", \"Exceptional battery life, often lasting up to two days on a single charge.\", \"Powerful and versatile camera system with a 200MP main sensor and impressive zoom capabilities.\"]', '[\"High price point, making it one of the most expensive non-folding smartphones.\", \"Absence of a headphone jack and microSD card slot.\", \"Large and bulky design, which might be challenging for one-handed use or users with smaller hands.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIqQwZI0WuCTplCeXTBoq47q5aIjHogPK_3N2Z-fWaGVR_PSdgWGuVR7dfQw&s', '1,521,862 (v10)', 'Consistently lasts close to two days on a single c', '4.5/5'),
(21, 'samsung galaxy s25 ultra 256gb', 'Samsung Galaxy S25 Ultra 256GB', '₹109,490', '86/100', 'February 2025', 'Snapdragon 8 Elite for Galaxy', 'Octa-core', '12GB', 'Dynamic LTPO AMOLED 2X', '3120 x 1440 pixels (QHD+)', '120Hz adaptive', '6.9 inches', '200MP f/1.7 (Wide)', '50MP f/1.9 (Ultra-Wide)', '50MP f/3.4 (5x Optical Telephoto) + 10MP f/2.4 (3x Optical Telephoto)', '12MP f/2.2', '5000 mAh', '45W wired, 15W wireless', '256GB', 'UFS 4.0 Flash', '[\"Excellent 6.9-inch QHD+ Dynamic LTPO AMOLED 2X display with 120Hz refresh rate and anti-reflective coating.\", \"Solid performance powered by the Snapdragon 8 Elite for Galaxy chipset.\", \"Improved camera array featuring a 200MP main sensor and a 50MP ultrawide lens.\"]', '[\"The S Pen has lost its Bluetooth functionality.\", \"Charging speeds, at 45W wired and 15W wireless, lag behind some rivals.\", \"Offers only minor hardware changes and a similar design compared to its predecessor.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRVECZyAyEmj_gAHR2G00AgJ4PK6Ge7tK_8FRbPlQ0LNjTgU05mWO6eulHQoQ&s', '3,135,223 (v11)', '13h 51m (PCMark)', '4.3/5'),
(22, 'apple iphone 16 pro max 256 gb', 'Apple iPhone 16 Pro Max 256 GB', '₹1,32,900', 'N/A', 'September 2024', 'Apple A18 Pro chip', 'Hexa-core (2x P-cores (4.02 GHz) + 4x E-cores (2.42 GHz))', '8 GB', 'LTPO Super Retina XDR OLED', '2868 x 1320 pixels (460 ppi)', 'ProMotion technology with adaptive refresh rates u', '6.9 inches', '48 MP, f/1.78 (wide)', '48 MP, f/2.2 (ultrawide, 120-degree FOV)', '12 MP, f/2.8 (periscope telephoto, 5x optical zoom)', '12 MP, f/1.9 (wide)', '4685 mAh', 'Fast-charge capable (up to 50% in 30 min with 20W+', '256 GB', 'NVMe', '[\"Excellent battery life, offering up to 33 hours of video playback.\", \"Features the largest and brilliant 6.9-inch Super Retina XDR OLED display with ProMotion technology.\", \"Powered by the powerful Apple A18 Pro chip and boasts an upgraded camera system with new features like a 48MP ultrawide lens and Camera Control button.\"]', '[\"Charging speeds remain relatively slow compared to some competitors.\", \"The larger 6.9-inch design can make it harder to use comfortably with one hand.\", \"Apple Intelligence features, while promising, were a work in progress at launch and lacked an immediate \'wow\' factor.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkjWIY9yKUP6j2fLJ3UNE5hJN1mzmRQyEfCo8HO_igkh3vK3OMnFkmr5UDmg&s', '2,079,833', 'Up to 33 hours video playback', '4.5/5'),
(23, 'samsung s25', 'Samsung Galaxy S25', '₹68,000', '92/100', 'February 2025', 'Qualcomm Snapdragon 8 Elite for Galaxy', 'Octa-core (2×4.47 GHz Oryon V2 Phoenix L + 6×3.53 GHz Oryon V2 Phoenix M)', '12GB', 'Dynamic LTPO AMOLED 2X', '1080x2340 px (FHD+)', '120 Hz', '6.2 inches (15.75 cm)', '50 MP Wide Angle Primary', '12 MP Ultra-Wide Angle', '10 MP Telephoto (3x Optical Zoom)', '12 MP', '4000 mAh', '25W Wired, 15W Wireless', '128GB, 256GB, 512GB', '...', '[\"Powered by the highly capable Qualcomm Snapdragon 8 Elite for Galaxy processor, offering significant performance improvements.\", \"Features an excellent 6.2-inch Dynamic LTPO AMOLED 2X display with a smooth 120Hz refresh rate, providing crisp visuals and vibrant colors.\", \"Boasts a compact size and premium design with improved durability, making it comfortable to hold and use.\"]', '[\"Battery life, while sufficient for casual users, is considered decent but lower than many competing smartphones in its segment.\", \"Offers mostly incremental upgrades from its predecessor, leading to an iterative design and fewer revolutionary changes.\", \"Charging speeds are capped at 25W wired and 15W wireless, which is slower compared to many rivals in the flagship category.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4k0heIzAdnLz5mjeqa1i5uR1JLJH2znUxOxHpA-BJlMEZC1X_zR_uqwGiCB8&s', '3,135,223 (v11)', '11 hours 49 minutes (PCMark test)', '4/5'),
(24, 'iphone 15 pro', 'iPhone 15 Pro', '₹89,994', '90/100', 'September 2023', 'Apple A17 Pro (3 nm)', 'Hexa-core (2x3.78 GHz + 4x2.11 GHz)', '8GB', 'LTPO Super Retina XDR OLED', '2556‑by‑1179-pixel resolution at 460 ppi', 'ProMotion technology with adaptive refresh rates u', '6.1‑inch', '48MP Main (ƒ/1.78, sensor-shift OIS)', '12MP Ultra Wide (ƒ/2.2, 120° FOV)', '12MP 3x Telephoto (ƒ/2.8, OIS)', '12MP (ƒ/1.9, autofocus with Focus Pixels)', '3,274 mAh', 'Fast charging (up to 29W)', '128GB (up to 1TB options available)', 'NVMe', '[\"Blazing performance with the A17 Pro chip.\", \"Versatile and excellent camera system with advanced features.\", \"Premium and lighter titanium design with a customizable Action button.\"]', '[\"Shorter battery life compared to the Pro Max and potential overheating issues.\", \"Limited optical zoom (3x) compared to the iPhone 15 Pro Max.\", \"Base 128GB storage might be insufficient for some users, and slower USB-C speeds compared to some competitors.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSknO33dClLxOzCtSlYZH3dp3kGNfjGdrOOAMgZCIIJWQq7ye0Yr7Apsd2HC0&s', '1,641,883 (v10)', 'Up to 16 hours 45 minutes video playback; generall', '4.5/5'),
(26, 'samsung galaxy s24', 'Samsung Galaxy S24', '₹42,990', 'N/A', 'January 2024', 'Exynos 2400', 'Deca Core (3.2 GHz, Single Core + 2.9 GHz, Dual core + 2.6 GHz, Tri core + 1.95 GHz, Quad core)', '8 GB', 'Dynamic AMOLED 2X', '1080 x 2340 pixels (FHD+)', '120 Hz adaptive', '6.2 inches', '50 MP (f/1.8)', '12 MP (ultrawide, f/2.2)', '10 MP (telephoto, 3x optical zoom, f/2.4)', '12 MP', '4000 mAh', '25W wired, 15W wireless, 4.5W reverse wireless', '128 GB', 'UFS 3.1/4.0', '[\"Strong performance for everyday tasks and gaming.\", \"Stunning and bright Dynamic AMOLED 2X display.\", \"Promises seven years of software and security updates.\"]', '[\"Relatively slow charging speeds compared to competitors (25W wired).\", \"Exynos 2400 processor in some regions (including India) may not be as efficient or powerful as the Snapdragon 8 Gen 3.\", \"No microSD card slot for expandable storage.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_LOntXvRpUR9M8evfnOgsMZTCl63N5xch_nWIYrP79yRLpN-DTj1KutJC5Zc&s', '2,011,752 (v11)', 'Up to 27 hours 28 minutes (video playback) and eas', '4.0/5'),
(28, 'samsung galaxy s25 256gb unlocked', 'Samsung Galaxy S25 256GB Unlocked', '₹74,999', '80/100', 'February 2025', 'Qualcomm Snapdragon 8 Elite for Galaxy', 'Octa-core (2x 4.47 GHz Oryon (Phoenix L) + 6x 3.53 GHz Oryon (Phoenix M))', '12 GB', 'Dynamic LTPO AMOLED 2X', '2340 x 1080', '120 Hz', '6.2 inches', '50 MP (wide)', '12 MP (ultrawide)', '10 MP (telephoto, 3x optical zoom)', '12 MP', '4000 mAh', '25W wired, 15W wireless', '256GB', 'UFS 4.0', '[\"Exceptional performance with Snapdragon 8 Elite for Galaxy\", \"Vibrant Dynamic LTPO AMOLED 2X display with 120Hz refresh rate\", \"Versatile camera system with AI enhancements and 3x optical zoom\"]', '[\"Relatively slow charging speeds compared to competitors\", \"Battery life could be better for power users\", \"Iterative design with limited hardware upgrades from its predecessor\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQX0Ju8kz5vRm1YuHf0w5KSvMECJMqM0m4_0ry3CGoBZ6VgTzxMdUMGudIzho&s', '3,135,223 (v11)', '15 hours 43 minutes', '4.6/5'),
(29, 'samsung a73', 'Samsung Galaxy A73 5G', '₹41,799', 'N/A', 'March 2022', 'Qualcomm Snapdragon 778G', 'Octa-core (1x 2.4 GHz Cortex-A78, 3x 2.4 GHz Cortex-A78, 4x 1.8 GHz Cortex-A55)', '8 GB', 'Super AMOLED Plus', '1080 x 2400 pixels (FHD+)', '120Hz', '6.7 inches', '108 MP, f/1.8 (wide), OIS', '12 MP, f/2.2 (ultrawide)', '5 MP, f/2.4 (macro)', '32 MP, f/2.2', '5000 mAh', '25W Fast Charging', '128 GB', 'UFS (expandable with microSD up to 1 TB)', '[\"Vibrant 120Hz Super AMOLED Plus display.\", \"Excellent battery life, often lasting up to two days with moderate usage.\", \"Versatile 108MP OIS quad-camera system.\"]', '[\"No charger included in the box.\", \"Lacks a 3.5mm headphone jack.\", \"No wireless charging support.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmOQlQPQ3Ge-YCUDEhSc36OoRSO6bRHxXGh1_fg8Z8n3qeUMxgWuvE2hpzYA&s', '579,837 (v10)', 'Up to 2 days with moderate usage, 7-8 hours screen', '80/100'),
(32, 'galaxy s25 plus phone', 'Samsung Galaxy S25 Plus', '₹74,999', 'N/A', 'February 2025', 'Qualcomm Snapdragon 8 Elite', 'Octa-Core 4.47GHz + 3.5GHz', '12 GB', 'Dynamic AMOLED 2X', '3120 x 1440 pixels (QHD+)', '120Hz Adaptive', '6.7 inches', '50 MP', '12 MP Ultra-Wide Angle', '10 MP Telephoto (3x Optical Zoom)', '12 MP', '4900 mAh', '45W Fast Charging', '256GB, 512GB', 'N/A', '[\"Powerful performance with Qualcomm Snapdragon 8 Elite SoC\", \"Excellent QHD+ Dynamic AMOLED 2X display with 120Hz refresh rate\", \"Versatile triple rear camera setup delivering sharp and vibrant photos and videos\"]', '[\"Camera hardware largely unchanged from the previous generation\", \"Durability with Gorilla Glass Victus 2 and IP68, while good, is not as advanced as some rivals offering IP69\", \"Benchmark scores, while high, may not be as high as some other Snapdragon 8 Elite-powered counterparts\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSReevz2s5RJbeDGx5amLWeMioOqq26bhBsDGphxICx5xnaWABRigQADbT8jGM&s', 'N/A', 'Around a full day of usage', 'N/A'),
(33, 'samsung galaxy s26 ultra', 'Samsung Galaxy S26 Ultra', '₹139,999', '99/100', 'March 2026', 'Qualcomm Snapdragon 8 Elite Gen 5 for Galaxy (3nm)', 'Octa-core (2x4.6GHz Oryon V3 Phoenix L + 6x3.62GHz Oryon V3 Phoenix M)', '12GB LPDDR5X', 'Dynamic LTPO AMOLED 2X', '1440x3120 px (QHD+)', '1-120Hz adaptive', '6.9 inches (17.53 cm)', '200 MP Wide Angle Primary Camera (F1.4, OIS)', '50 MP Ultra-Wide Angle Camera (F1.9)', '50 MP Telephoto (5x Optical Zoom, F2.9, OIS)', '12 MP (F2.2)', '5000mAh', '60W wired, 25W wireless', '512GB', 'UFS 4.0', '[\"World\'s first built-in Privacy Display for enhanced security.\", \"Powered by the most powerful mobile chip, Snapdragon 8 Elite Gen 5 for Galaxy.\", \"Massive camera upgrades, including a 200MP F1.4 main sensor for superior low-light photography.\"]', '[\"Charger is not included in the box.\", \"No option for expandable storage via a card slot.\", \"Battery life, while improved, is still behind some rival flagship phones.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkDf4r08NojgKkTgPdKFFn0sgFzTqJfQ60-qSq-CHjDnvGfsL-R1xFsFCA6A&s', '4,027,702 (v11)', '16 hours and 10 minutes', '4.5/5'),
(34, 'samsung s22', 'Samsung Galaxy S22', '₹72,999', 'N/A', 'February 2022', 'Qualcomm Snapdragon 8 Gen 1 / Samsung Exynos 2200', 'Octa-core', '8 GB', 'Dynamic AMOLED 2X', '1080 x 2340 pixels', '120Hz adaptive', '6.1 inches', '50 MP, f/1.8, OIS (wide)', '12 MP, f/2.2 (ultrawide)', '10 MP, f/2.4, 3x optical zoom, OIS (telephoto)', '10 MP, f/2.2, AF', '3700 mAh', '25W Fast Charging', '128GB, 256GB', 'UFS', '[\"Compact flagship design and premium build quality.\", \"Excellent Dynamic AMOLED 2X display with 120Hz refresh rate.\", \"Versatile and high-quality triple camera system.\"]', '[\"Sub-par battery life.\", \"Slower charging speeds compared to some rivals.\", \"Tendency to heat up and performance throttling under heavy load.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcPFQSebzXeFd7FL4d2J0WGSfh0Vy72qrOJY1NUe_NBeAtA2TbzfPMAmzIxPQ&s', '1,022,200 (v10)', 'Around 7-8 hours of screen-on time with mixed usag', '3.75/5'),
(35, 'motorola moto edge 50 fusion 5', 'Motorola Edge 50 Fusion', '₹18,999', '85/100', 'May 2024', 'Qualcomm Snapdragon 7s Gen 2', 'Octa-core (4x2.40 GHz Cortex-A78 & 4x1.95 GHz Cortex-A55)', '8GB, 12GB', 'P-OLED', '1080 x 2400 pixels (FHD+)', '144Hz', '6.7 inches', '50MP (Sony Lytia 700C, f/1.8, OIS)', '13MP (Ultrawide, f/2.2, 120-degree FOV, Macro Vision)', 'N/A', '32MP (f/2.4)', '5000 mAh', '68W TurboPower', '128GB, 256GB, 512GB', 'UFS 2.2', '[\"Lightweight and slim design with IP68 rating.\", \"Smooth 144Hz pOLED display.\", \"Excellent battery life with 68W fast charging.\"]', '[\"Performance is average compared to competitors in the price range.\", \"No microSD card slot.\", \"No 3.5mm headphone jack and no wireless charging.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2yoag3j86ZFcHI57LN6b1GsJyVGtFSHs-ZEdU9sW9bZVPB72tZXyma89OREA&s', '620,648 (v10)', 'Over 30 hours (typical usage), 9h 53m (PCMark)', '3.9/5'),
(36, 'celular samsung a73 5g', 'Samsung Galaxy A73 5G', '₹41,799', 'N/A', 'March 2022', 'Qualcomm Snapdragon 778G (6nm)', 'Octa-core (1x 2.4 GHz Cortex-A78, 3x 2.4 GHz Cortex-A78, 4x 1.8 GHz Cortex-A55)', '8GB', 'Super AMOLED Plus', '1080 x 2400 pixels (FHD+)', '120 Hz', '6.7 inches', '108MP (f/1.8, OIS)', '12MP ultrawide (f/2.2)', '5MP macro (f/2.4)', '32MP (f/2.2)', '5000 mAh', '25W wired fast charging', '128GB', 'N/A', '[\"Beautiful and smooth 120Hz Super AMOLED Plus display\", \"Excellent 108MP main camera with OIS\", \"Long-lasting 5000mAh battery\"]', '[\"No 3.5mm headphone jack\", \"Charger not included in the box\", \"Slow 25W charging speed compared to rivals\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmOQlQPQ3Ge-YCUDEhSc36OoRSO6bRHxXGh1_fg8Z8n3qeUMxgWuvE2hpzYA&s', '579,837 (v10)', 'Up to 2 days with light usage, 7-8 hours screen-on', '4/5'),
(37, 'xiaomi redmi 8 pro', 'Xiaomi Redmi Note 8 Pro', '₹9,490', '80/100', 'September 2019', 'MediaTek Helio G90T', 'Octa-core (Dual 2.05GHz A76 + Hexa 2GHz A55)', '6GB', 'IPS LCD', '1080 x 2340 pixels', '60Hz', '6.53 inches', '64MP', '8MP Ultra-Wide', '2MP Macro + 2MP Depth', '20MP', '4500 mAh', '18W Fast Charging', '64GB', 'UFS 2.1', '[\"Very good battery life.\", \"Powerful MediaTek Helio G90T processor for gaming.\", \"64MP main camera performs well in daylight.\"]', '[\"MIUI is riddled with bloatware and ads.\", \"Photo quality decreases in low light conditions, especially ultra-wide and macro cameras are not very useful.\", \"Fingerprint scanner placement inside the rear camera frame.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOTggr67xmyeGNCPBDlhTvfSUjSKdOp1FOiIFfXyMpHQrn_nIVeGCMjZdsJCc&s', '369361', '10h 54m (PCMark)', '4.0/5'),
(39, 'xiaomi redmi 9 pro', 'Redmi Note 9 Pro', '₹11,499', '92/100', 'March 2020', 'Qualcomm Snapdragon 720G', 'Octa-core (2x 2.3 GHz Kryo 465 Gold & 6x 1.8 GHz Kryy 465 Silver)', '4GB, 6GB', 'IPS LCD', '1080x2400 pixels', '60Hz', '6.67 inches', '48MP', '8MP (Ultra-wide)', '5MP (Macro)', '16MP', '5020mAh', '18W Fast Charging', '64GB, 128GB', 'UFS 2.1', '[\"Long-lasting 5020mAh battery\", \"Good performance from Snapdragon 720G processor\", \"Premium design and build quality\"]', '[\"60Hz refresh rate display\", \"Ordinary camera performance, especially in low light\", \"Large and heavy form factor\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZ8AqHqh_n9sE5CDF1NCyGl66A4kjLeFgtUx4T6LLrsh0RGfRR-bVJ--9Uv2Y&s', '393,368', '2-3 days with average use, up to 15 hours screen-o', '4.0/5'),
(40, 'iphone 16', 'iPhone 16', '₹64,900', '92/100', 'September 2024', 'Apple A18', 'Hexa-core CPU, 5-core GPU', '8 GB LPDDR5X', 'Super Retina XDR OLED', '2556×1179 pixels (~460 ppi)', '60 Hz', '6.1 inches', '48 MP Fusion, f/1.6, sensor-shift OIS', '12 MP Ultrawide, f/2.2, 120° FoV', 'N/A', '12 MP, f/1.9, autofocus', '13.84 Wh (3561 mAh)', 'MagSafe and Qi2 wireless, USB-C fast-charge (up to', '128 GB, 256 GB, 512 GB', 'NVMe', '[\"Powerful A18 chipset and 8GB RAM for swift performance.\", \"Excellent cameras with improved features and spatial video capture.\", \"Solid battery life, offering up to 22 hours of video playback.\"]', '[\"Display retains a 60Hz refresh rate, unlike many competitors.\", \"Camera Control button can be finicky in use.\", \"Charging speeds, while improved, could be faster compared to some rivals.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZX4yZ3deF-y2IULXDsZvt8AQOVrba6qN8bg4HGldtPE2AnnjtS0471STXK5s&s', '1,943,775 (v11)', 'Up to 22 hours video playback', '4.0/5'),
(42, 'iphone 17', 'iPhone 17', '₹82,900', 'N/A', 'September 2025', 'Apple A19 SoC', '5-core GPU', '8 GB', 'LTPO Super Retina XDR OLED', '2622 × 1206 pixels (~460 ppi)', '120Hz ProMotion', '6.3-inch', '48MP Fusion Main (ƒ/1.6 aperture, sensor-shift OIS, 2x optical-quality telephoto)', '48MP Fusion Ultra Wide (ƒ/2.2 aperture, 120° FOV)', 'N/A', '18MP Centre Stage with Dual Capture', '3692 mAh', 'Fast charging (50% in ~30 minutes), MagSafe (15W)', '256 GB, 512 GB', 'NVMe (estimated)', '[\"Advanced Display: Features a larger 6.3-inch Super Retina XDR OLED display with a 120Hz ProMotion adaptive refresh rate, a first for a non-Pro iPhone model.\", \"Powerful Performance: Equipped with the new Apple A19 SoC, delivering significantly faster performance and greater power efficiency.\", \"Enhanced Camera System: Boasts a revolutionary 48MP Dual Fusion camera system, including a 48MP Fusion Main lens with 2x optical-quality telephoto and a 48MP Fusion Ultra Wide camera.\"]', '[\"Higher Starting Storage/Price: Removes the 128GB storage option, with the base model starting at 256GB, potentially leading to a higher entry price for some users.\", \"Third-Party Modem: Opts for Qualcomm\'s Snapdragon X80 modem instead of Apple\'s newer C1X modem, which might be seen as a compromise in connectivity technology.\", \"Regional Price Disparity: Indian market prices are notably higher compared to the USA, making it a more expensive purchase in India.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMznR-9KS05jVR-oP9Xp05Zp-o1KvqrVohvkKq_PIOe-1pN4eeiG7OlCoFLw&s', 'N/A', 'Up to 30 hours video playback', 'N/A'),
(43, 'iphone 17 5g 256gb sage', 'iPhone 17 5G 256GB Sage', '₹78,900', 'N/A', 'September 2025', 'Apple A19 Chip', 'Hexa-core CPU, 5-core GPU', '8GB', 'Super Retina XDR OLED with ProMotion', '2622 x 1206 pixels at 460 ppi', 'Up to 120Hz adaptive', '6.3-inch', '48MP Fusion Main (f/1.6, sensor-shift OIS, 2x optical-quality telephoto enabled)', '48MP Fusion Ultra Wide (f/2.2, 120° FOV)', 'N/A', '18MP Center Stage camera (f/1.9, autofocus)', '3692 mAh', 'Up to 50% in 20 minutes with 40W adapter (wired), ', '256GB', 'NVMe', '[\"Stunning 6.3-inch Super Retina XDR display with 120Hz ProMotion for smooth visuals.\", \"Powered by the advanced A19 Bionic chip with a 5-core GPU for exceptional performance.\", \"Versatile 48MP Dual Fusion camera system delivers super-high-resolution photos and 2x optical-quality zoom.\"]', '[\"High price point in the Indian market compared to some competitors.\", \"Charging adapter is not included in the box, requiring a separate purchase.\", \"Lacks a 3.5mm headphone jack and expandable storage options.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbjwqKr-uQOd7LNTQdB8cZi5cTId-y4fzeOcgyoF61mKA373mS36o2M3feVw&s', 'N/A', 'Up to 30 hours of video playback', 'N/A'),
(51, 'vivo v70 elite', 'Vivo V70 Elite', '₹51,999', 'N/A', 'February 2026', 'Qualcomm Snapdragon 8s Gen 3', 'Octa Core', '8GB', 'AMOLED', '1260x2750 pixels', '120Hz', '6.59 inches', '50MP Wide Angle Primary Camera (with OIS)', '50MP Telephoto Camera (3x Optical Zoom, 100x Digital Zoom)', '8MP Ultra-Wide Angle Camera', '50MP ZEISS Group Selfie Camera', '6500 mAh', '90W Fast Charging', '256GB', 'UFS 4.1', '[\"Strong camera system with ZEISS optics and OIS for detailed shots across lighting conditions.\", \"Bright and sharp 120Hz AMOLED display with up to 5000 nits peak brightness for excellent outdoor visibility.\", \"Long-lasting 6500 mAh battery with 90W fast charging, comfortably lasting a full day with heavy usage.\"]', '[\"Performance, while dependable, may not match some competitors with newer chipsets in the same price range.\", \"Some low-light camera shots may show grain, and gaming is capped at 90FPS in BGMI.\", \"The software experience with OriginOS 6 can be relatively cluttered.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQegIe1UPjWNfEP6TgnzlK6msIwIpAGTHntClfez6og7eXO3itOqxfS6aieMg&s', '1,834,182 (v11)', 'Over 18 hours (PCMark test), comfortably lasting a', '4.4/5'),
(53, 'iqoo 15r', 'iQOO 15R', '₹44,998', 'N/A', 'February 2026', 'Qualcomm Snapdragon 8 Gen 5', 'Octa Core', '8GB', 'AMOLED', '1.5K (2750x1260 pixels)', '144Hz', '6.59-inch', '50MP Sony LYT-700V (with OIS)', '8MP ultrawide', 'N/A', '32MP', '7600mAh', '100W Flash Charging', '256GB', 'UFS 4.1', '[\"Powerful Qualcomm Snapdragon 8 Gen 5 processor for flagship-level performance.\", \"Massive 7600mAh battery with 100W fast charging support.\", \"High refresh rate 1.5K AMOLED display with up to 5000 nits peak brightness.\"]', '[\"Camera app lacks variety of modes and filters compared to some similarly priced smartphones.\", \"The 144Hz refresh rate is capped at 120Hz for system UI and most apps, only reaching 144Hz for select games in \'Monster\' mode.\", \"Dual rear camera setup might be considered less versatile than triple camera setups found on some competitors.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbZeZSLE9DTx3elQHCh8C6_wbd8X1FOUSAp1juYl0vuoC_6UPfYp0XgfdQ9pw&s', '3,078,708', 'Up to 3.1 hours of gaming, 7.1 hours of social med', 'N/A'),
(55, 'motorola signature', 'Motorola Signature', '₹54,348', 'N/A', 'January 2026', 'Snapdragon 8 Gen 5', 'Octa-core (2x3.8 GHz Oryon Gen 3 & 6x3.3 GHz Oryon Gen 3)', '12GB, 16GB LPDDR5X', 'LTPO AMOLED', '1264x2780 pixels (QHD)', '165Hz (LTPO)', '6.8 inches', '50MP (Sony LYT-828, f/1.6)', '50MP (Telephoto, f/2.0)', '50MP (Ultrawide, f/2.2)', '50MP (Sony LYT-500, f/2.0)', '5200mAh (Silicon-Carbon)', '90W wired, 50W wireless', '256GB, 512GB, 1TB', 'UFS 4.1', '[\"Excellent camera system with four 50MP lenses, including a main Sony LYT-828 sensor.\", \"Stunning 165Hz LTPO AMOLED display with QHD resolution and high brightness.\", \"Powerful Snapdragon 8 Gen 5 processor delivering flagship-grade performance and offering 7 years of software updates.\"]', '[\"Battery life, while decent, can be modest compared to some rival flagships.\", \"Software experience needs more polish and includes some pre-installed bloatware.\", \"The rear finish might not feel ultra-premium to all users, despite the overall sleek design.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtBKdGGH0Asjh-tB4JikQ3ZDQ_orrMc7fEHKv2YD5Vn2FrTCSGZ-CJQVCz-w&s', '3,258,670 (v11)', 'Up to 52 hours (mixed use) / 12h 53m (PCMark)', 'N/A'),
(57, 'oneplus 11r', 'OnePlus 11R', '₹27,999', '85/100', 'February 2023', 'Qualcomm Snapdragon 8+ Gen 1 (4nm)', 'Octa-core (1x Cortex-X2 @ 3.2 GHz, 3x Cortex-A710 @ 2.75 GHz, 4x Cortex-A510 @ 2.00 GHz)', 'Up to 18GB LPDDR5X', '6.74-inch Super Fluid AMOLED', '2772 x 1240 pixels (1.5K)', '120Hz', '6.74 inches', '50MP (Sony IMX890, OIS)', '8MP (Ultra-wide angle)', '2MP (Macro)', '16MP (Wide Angle Lens)', '5000 mAh', '100W SuperVOOC Fast Charging', 'Up to 512GB', 'UFS 3.1', '[\"Great performance with Snapdragon 8+ Gen 1 chipset.\", \"Premium design and beautiful curved AMOLED display.\", \"Excellent battery life with 100W SuperVOOC fast charging.\"]', '[\"Lackluster secondary (ultra-wide and macro) cameras.\", \"No official IP rating for dust and water resistance.\", \"No wireless charging support.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHvo-X0T0D2wVpd3uEXHRvTLTbJdbNV41hnK559iXlP6Cn43IE7F4K2XvlSXg&s', '1,299,948 (v10)', 'Excellent, typically lasting a full day with heavy', '8.5/10'),
(59, 'oneplus 15r', 'OnePlus 15R', '₹47,998', 'N/A', 'December 2025', 'Qualcomm Snapdragon 8 Gen 5', 'Octa-core (2 x 3.8 GHz Qualcomm Oryon Gen 3, 6 x 3.3 GHz Qualcomm Oryon Gen 3)', '12GB LPDDR5X Ultra', 'LTPS AMOLED', '1272x2800 pixels (1.5K)', '165 Hz', '6.83-inch', '50MP (f/1.8, Sony IMX906) with OIS', '8MP (f/2.2, Ultrawide)', 'None', '32MP', '7,400mAh', '80W SuperVOOC Fast Charging', '256GB, 512GB', 'UFS 4.1', '[\"Near-flagship performance with Qualcomm Snapdragon 8 Gen 5 processor.\", \"Outstanding battery life with a 7,400mAh capacity and 80W fast charging.\", \"Smooth 165Hz AMOLED display with excellent brightness.\"]', '[\"Lack of a telephoto camera and a basic ultrawide camera.\", \"Noticeable price increase compared to its predecessor.\", \"Some thermal throttling observed under heavy workloads.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGRpLvnN68PCjcq__upCFPgX_qBKTzgpqgj7g7LQWKu6EtrTIsKuujEhiQzp8&s', '2,957,229 (v10)', 'Up to 23 hours (PCMag test), 18 hours 13 minutes (', '8.5/10'),
(61, 'oneplus 15', 'OnePlus 15', '₹72,999', '82/100', 'November 2025', 'Qualcomm Snapdragon 8 Elite Gen 5', 'Octa Core', '12GB LPDDR5X', 'LTPO AMOLED', '2772 x 1272 pixels', '165Hz', '6.78 inches', '50MP (Sony IMX906, OIS)', '50MP (Ultra-wide, OV50D)', '50MP (Periscopic Telephoto, 3.5x optical zoom, S5KJN5)', '32MP (with autofocus and custom RGBW sensor)', '7,300mAh', '120W SUPERVOOC (wired), 50W AIRVOOC (wireless)', '256GB', 'UFS 4.1', '[\"Ultra-long battery life with 7,300mAh capacity and 120W fast charging.\", \"Powered by the latest Qualcomm Snapdragon 8 Elite Gen 5 processor for flagship-tier performance.\", \"Features a silky-smooth 165Hz LTPO AMOLED display with an industry-leading 3200Hz touch sampling rate.\"]', '[\"Display resolution is downgraded to 1.5K from 2K compared to its predecessor.\", \"Lacks expandable storage, with no memory card slot.\", \"The 1TB storage option is not available for global markets.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs1RIVMUcBoCBJHVQiKTZ5iqldI_OSZQIVhPPfKPDziPrwq23ifVsk7_avMQk&s', '3,615,565', '26 hours, 11 minutes', '4.1/5'),
(63, 'sumsung galaxy s24 ultra 5g', 'Samsung Galaxy S24 Ultra 5G', '₹93,999', '98/100', 'January 2024', 'Qualcomm Snapdragon 8 Gen 3 for Galaxy (SM8650-AC)', '1x 3.4 GHz Cortex-X4, 3x 3.15 GHz Cortex-A720, 2x 2.96 GHz Cortex-A520, 2x 2.27 GHz Cortex-A520', '12 GB', 'Dynamic LTPO AMOLED 2X', '1440 x 3120 pixels', '120Hz', '6.8 inches', '200 MP', '12 MP Ultra-Wide Angle Camera', '50 MP (5x Optical Zoom) Telephoto Camera', '12 MP', '5000 mAh', '45W Fast Charging', '256 GB', 'UFS 4.0', '[\"Excellent performance and long battery life.\", \"Versatile and high-quality camera system, especially for zoom.\", \"Premium and durable design with titanium frame and S Pen.\"]', '[\"No microSD card slot and no audio jack.\", \"Large and heavy build.\", \"Relatively slow charging speeds compared to some competitors.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_LOntXvRpUR9M8evfnOgsMZTCl63N5xch_nWIYrP79yRLpN-DTj1KutJC5Zc&s', '2026663', 'Over 16 hours (web browsing) or up to 34 hours 36 ', '4.5/5');
INSERT INTO `compare_device_cache` (`id`, `search_query`, `name`, `price`, `spec_score`, `release_date`, `processor`, `cores`, `ram`, `disp_type`, `disp_res`, `disp_refresh`, `disp_size`, `cam_main`, `cam_sec`, `cam_tert`, `cam_front`, `bat_capacity`, `bat_charging`, `storage_internal`, `storage_type`, `pros`, `cons`, `image_url`, `antutu_score`, `battery_life`, `expert_score`) VALUES
(64, 'iphone 16 pro max', 'iPhone 16 Pro Max', '₹134,900', 'N/A', 'September 2024', 'Apple A18 Pro chip', '6-core CPU (2 performance + 4 efficiency), 6-core GPU, 16-core Neural Engine', '8 GB LPDDR5X', 'Super Retina XDR OLED', '2868x1320 pixels at 460 ppi', 'ProMotion technology with adaptive refresh rates u', '6.9-inch (diagonal)', '48 MP Wide Angle Primary Camera, ƒ/1.78 aperture, second-generation sensor-shift optical image stabi', '48 MP Ultra-Wide Angle Camera with 120-degree field of view', '12 MP Telephoto (up to 25x Digital Zoom, up to 5x Optical Zoom) Camera', '12 MP TrueDepth Camera', '4685 mAh', 'MagSafe wireless charging up to 25W, Qi2 wireless ', '256GB, 512GB, 1TB', 'NVMe', '[\"Powered by the highly efficient Apple A18 Pro chip, offering excellent performance and advanced Apple Intelligence features.\", \"Features a versatile and upgraded camera system with a 48MP main sensor, 48MP ultra-wide lens, and 5x optical zoom telephoto, capable of 4K 120 fps Dolby Vision video recording.\", \"Boasts a large and immersive 6.9-inch Super Retina XDR OLED display with a 120Hz ProMotion adaptive refresh rate and minimal bezels for a superior viewing experience.\"]', '[\"The iPhone 16 Pro Max comes with a premium price tag, especially for higher storage configurations, making it a significant investment.\", \"The device exclusively supports eSIM, which might be a drawback for users who prefer or require a physical SIM card slot.\", \"Some advanced Apple Intelligence features were rolled out in phases, meaning not all functionalities were immediately available at the time of release.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkjWIY9yKUP6j2fLJ3UNE5hJN1mzmRQyEfCo8HO_igkh3vK3OMnFkmr5UDmg&s', '2,079,833', 'Up to 33 hours video playback, up to 29 hours stre', 'N/A'),
(65, 'pixel 10a', 'Google Pixel 10a', '₹49,999', '...', 'March 2026', 'Google Tensor G4', '...', '8 GB', 'pOLED Actua display', '1080x2424 pixels', '120Hz', '6.3 inch', '48MP f/1.7 (wide)', '13MP f/2.2 (ultrawide)', 'N/A', '13MP f/2.2', '5100mAh', '30W wired, 10W wireless', '128 GB / 256 GB', 'UFS 3.1', '[\"Powered by the Google Tensor G4 chip, offering advanced AI features and Gemini integration.\", \"Equipped with an excellent camera system, featuring a 48MP main and 13MP ultrawide lens for high-quality photography.\", \"Features a durable design with Gorilla Glass 7i, IP68 water and dust resistance, and a long-lasting 5100mAh battery.\"]', '[\"Offers minimal upgrades over its predecessor, the Pixel 9a, with largely identical internal hardware and camera system.\", \"Lacks a dedicated telephoto lens, which is a notable omission at its price point.\", \"The Tensor G4 processor may not match the raw CPU/GPU performance of some competitors, and benchmark applications are blocked at launch.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlWaE401daDkeRWrLxiJdUlWFceuIWErcdKH5-vnLZA18QWvLKFpvfFYCr3Q&s', '1,400,792', '30+ hours (up to 120 hours with Extreme Battery Sa', '...'),
(67, 'samsung galaxy s26', 'Samsung Galaxy S26', '₹87,999', '...', 'March 2026', 'Qualcomm Snapdragon 8 Elite Gen 5 (North America, China, Japan) / Samsung Exynos 2600 (Global)', 'Octa-core (expected)', '12GB LPDDR5X', 'Dynamic LTPO AMOLED 2X', '2340x1080px (FHD+)', '120 Hz adaptive', '6.3 inches', '50MP (f/1.8, 1/1.56-inch sensor, Dual Pixel PDAF, OIS)', '12MP ultrawide (1/2.55-inch sensor, 120-degree FoV)', '10MP telephoto (1/3.94-inch sensor, 3x optical zoom)', '12MP', '4300 mAh', '25W wired, 15W wireless', '256GB/512GB', 'UFS (expected)', '[\"Equipped with the latest generation flagship processor, offering powerful performance.\", \"Features a vibrant Dynamic LTPO AMOLED 2X display with a smooth 120Hz adaptive refresh rate.\", \"Comes with an improved 4300 mAh battery capacity compared to its predecessor.\"]', '[\"Charging speeds (25W wired, 15W wireless) may not be as fast as some competing flagship smartphones.\", \"The chipset split (Exynos in some regions) could lead to potential performance inconsistencies across markets.\", \"Does not offer expandable storage via a microSD card.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxlxXCI3LOZYq4lNzHNrJT-yEfSAn_r2DcCbzaztwsmYJpYiZ0tAn5LgZNFw&s', '...', '...', '.../5'),
(69, 'samsung s24 ultra', 'Samsung Galaxy S24 Ultra', '₹119,999', '99/100', 'January 2024', 'Qualcomm Snapdragon 8 Gen 3 for Galaxy (SM8650-AC)', '1x 3.4 GHz Cortex-X4, 3x 3.15 GHz Cortex-A720, 2x 2.96 GHz Cortex-A520, 2x 2.27 GHz Cortex-A520', '12GB', 'Dynamic LTPO AMOLED 2X', '1440 x 3120 pixels (QHD+)', '120Hz', '6.8 inches', '200 MP, f/1.7 (wide), OIS', '50 MP, f/3.4 (periscope telephoto, 5x optical zoom), OIS', '10 MP, f/2.4 (telephoto, 3x optical zoom), OIS', '12 MP, f/2.2 (wide), Dual Pixel PDAF', '5000 mAh', '45W wired, 15W wireless, 4.5W reverse wireless', '256GB', 'UFS 4.0', '[\"Exceptional Dynamic LTPO AMOLED 2X display with high brightness and anti-glare coating.\", \"Powerful Snapdragon 8 Gen 3 for Galaxy processor delivering top-tier performance and long-lasting battery life.\", \"Versatile quad-camera system with a 200MP main sensor, improved 5x telephoto, and advanced AI features.\"]', '[\"High price point, making it less accessible compared to some competitors.\", \"Charging speeds are not class-leading when compared to some rival flagship smartphones.\", \"Design is largely similar to its predecessor, the S23 Ultra, offering less visual innovation.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_LOntXvRpUR9M8evfnOgsMZTCl63N5xch_nWIYrP79yRLpN-DTj1KutJC5Zc&s', '1,915,536 (v10)', 'Up to 16 hours 45 minutes of web browsing (5G)', '4.95/5'),
(70, 'apple iphone 16 pro max', 'Apple iPhone 16 Pro Max', '₹134,900', '92/100', 'September 2024', 'A18 Pro chip (New 6-core CPU with 2 performance and 4 efficiency cores, New 6-core GPU, New 16-core ', '6-core CPU, 6-core GPU, 16-core Neural Engine', '8 GB', 'Super Retina XDR OLED', '2868 × 1320 pixels (460 ppi)', 'Up to 120Hz ProMotion', '6.9-inch', '48 MP Wide Angle', '48 MP Ultra-Wide Angle', '12 MP Telephoto (5x optical zoom, up to 25x digital zoom)', '12 MP Wide Angle Lens', '4685 mAh', '20W Fast Charging (USB Type-C)', '256GB, 512GB, 1TB', 'NVMe', '[\"Largest and glorious Super Retina XDR OLED display.\", \"Epically long battery life, offering multi-day usage.\", \"Excellent cameras with significant upgrades, including a 48MP ultrawide lens and 5x optical zoom.\"]', '[\"Very expensive, with a high starting price.\", \"Large and heavy frame, which can be difficult to hold and carry for some users.\", \"Charging speeds are considered slow compared to competitors.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkjWIY9yKUP6j2fLJ3UNE5hJN1mzmRQyEfCo8HO_igkh3vK3OMnFkmr5UDmg&s', '2,079,833', 'Up to 33 hours video playback, 20-24 hours typical', '4.2/5'),
(71, 'samsung s25 ultra', 'Samsung Galaxy S25 Ultra', '₹106,000', '87/100', 'February 2025', 'Snapdragon 8 Elite for Galaxy', 'Octa-core', '12GB', 'Dynamic LTPO AMOLED 2X', '1440x3120 pixels (QHD+)', '120Hz (adaptive 1-120Hz)', '6.9-inch', '200MP (f/1.7) Wide Angle Primary Camera', '50MP Ultra-Wide Angle Camera (f/1.9)', '50MP Telephoto (5x Optical Zoom, f/3.4) + 10MP Telephoto (3x Optical Zoom, f/2.4)', '12MP (f/2.2) Wide Angle Lens', '5000mAh', '45W Fast Charging (wired), 25W Wireless Charging (', '256GB', 'UFS 4.0', '[\"Powerful Snapdragon 8 Elite for Galaxy processor for top-tier performance.\", \"Versatile quad-camera system with a 200MP main sensor and improved ultrawide.\", \"Stunning 6.9-inch Dynamic LTPO AMOLED 2X display with 120Hz refresh rate and high brightness.\"]', '[\"High price point, even with discounts.\", \"Charging speeds are not significantly improved compared to some rivals.\", \"Large form factor may impact portability for some users.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5EK6kaqgCr-Nuha8GeXgbOef-EweVJo8-tv9x-M1OmPpWAE8Gdu25ESC_4aI&s', '3,135,223 (v11)', 'Up to 31 hours (video playback), 17 hours 15 minut', '8.6/10'),
(73, 'apple iphone 15 pro max', 'Apple iPhone 15 Pro Max', '₹1,34,900', 'N/A', 'September 2023', 'A17 Pro chip', '6-core CPU (2 performance + 4 efficiency)', '8GB', 'LTPO Super Retina XDR OLED', '2796 x 1290 pixels (~460 ppi)', '120Hz adaptive (ProMotion)', '6.7-inch', '48MP, f/1.78, sensor-shift OIS', '12MP Ultra Wide, f/2.2, 120˚ FOV', '12MP 5x Telephoto, f/2.8, 3D sensor-shift OIS', '12MP, f/1.9, autofocus', '4422 mAh', 'Fast-charge capable (up to 50% in ~30 min with 20W', '256GB, 512GB, 1TB', 'NVMe', '[\"Fast, smooth performance with A17 Pro chip\", \"Exceptional camera system with 5x telephoto zoom\", \"Excellent long battery life\"]', '[\"High price\", \"Large size can be challenging for one-handed use\", \"Charging speed not as fast as some competitors\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQNwAFQHqnB2PPLzqzuZSSbJwb2H94sjH_aQuqlbgCXos4XcJmIVB15nmo7w&s', '1,641,883 (v10)', 'Up to 29 hours video playback; up to 95 hours audi', '4.5/5'),
(75, 'realme p4 power', 'realme P4 Power 5G', '₹24,485', '82/100', 'January 2026', 'MediaTek Dimensity 7400 Ultra 5G', 'Octa Core', '8GB, 12GB LPDDR4X', 'AMOLED HyperGlow 4D Curve+', '1280 x 2800 Pixels (1.5K FHD+)', '144Hz', '6.8-inch (17.27 cm)', '50MP (Sony primary sensor, f/1.8, OIS)', '8MP (Ultra-wide, f/2.2)', 'N/A', '16MP (f/2.4)', '10,001mAh', '80W SuperVOOC (wired), 27W reverse charging', '128GB, 256GB', 'UFS 3.1', '[\"Massive 10,001mAh battery with exceptional battery life, offering over two days of mixed usage.\", \"Vibrant 144Hz 1.5K AMOLED HyperGlow 4D Curve+ display with up to 6500 nits peak brightness and Corning Gorilla Glass 7i protection.\", \"Powerful MediaTek Dimensity 7400 Ultra 5G processor, coupled with a HyperVision+ AI chip, ensures smooth performance and supports 90fps BGMI gaming.\"]', '[\"Features a single bottom-firing speaker, which can be easily muffled and leads to a noticeable drop in audio quality.\", \"Camera performance is considered decent but heavily relies on post-processing, and the device lacks a tertiary rear camera.\", \"Does not support expandable storage via a microSD card slot.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4i4OY1qYv4Sp_ZSdvo9TXGG3iooenDQfN-fxR0U0-zBShi2MokVqAhyRYQQ&s', '1,047,842 (v11)', 'Over 2 days of mixed usage (25+ hours active use)', '8.2/10'),
(76, 'motorola edge 70', 'Motorola Edge 70', '₹29,948', 'N/A', 'November 2025', 'Qualcomm Snapdragon 7 Gen 4 SoC', 'Octa-core (1x2.8GHz Cortex-720 & 4x2.4GHz Cortex-720 & 3x1.8GHz Cortex-520)', '12GB', 'P-OLED', '2712x1220 (1.5K)', '120Hz', '6.7-inch', '50MP, f/1.8 with PDAF, OIS', '50MP, f/2.0 ultrawide with PDAF', 'N/A', '50MP, f/2.0', '5000mAh', '68W fast charging', '512GB', 'UFS 3.1', '[\"Ultra-slim build and unique textured back panel for a premium feel.\", \"Features IP68/IP69 dust and water resistance, MIL-STD-810H certification, and Gorilla Glass 7i for enhanced durability.\", \"Offers decent performance for daily tasks and a long-lasting battery life.\"]', '[\"Performance may not be optimal for power users in its price segment.\", \"The device can warm up quickly during intensive gaming sessions.\", \"Macro photography capabilities could be improved.\"]', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmSJJ3ggMF9NUmEhEzPl1M7OTDYjDVT1_BW9vyFQa4O5eZZHelJKJukwOACw&s', '9,56,920', 'Long-lasting', 'N/A'),
(77, 'apple iphone 17 pro max', 'Apple iPhone 17 Pro Max', '₹149,900', 'N/A', 'September 2025', 'Apple A19 Pro', 'Six-core CPU, six-core GPU, 16-core Neural Engine', '12 GB LPDDR5X', 'LTPO Super Retina XDR OLED', '2868 × 1320-pixel resolution at 460 ppi', 'ProMotion technology with adaptive refresh rates u', '6.9-inch (175 mm)', '48MP Fusion Main, f/1.78, 24mm (wide) with second‑generation sensor‑shift optical image stabilizatio', '48MP Fusion Ultra Wide, f/2.2, 13mm (ultrawide) with 120° field of view', '48MP Fusion Telephoto, f/2.8, 100mm (periscope telephoto) with 4x optical zoom (up to 8x optical-qua', '18MP Centre Stage camera, f/1.9, 23 mm (wide)', '4832 mAh', '40W fast charging (up to 50% in 20 minutes), MagSa', '256 GB, 512 GB, 1 TB, 2 TB', 'NVMe', '[\"Powered by the highly capable Apple A19 Pro chip, offering excellent performance.\", \"Features an advanced 48MP Pro Fusion camera system with significant improvements in telephoto capabilities.\", \"Boasts a brilliant 6.9-inch Super Retina XDR OLED display with up to 3000 nits peak brightness and a 120Hz ProMotion adaptive refresh rate.\"]', '[\"Comes with a high price point, making it a significant investment.\", \"Offers incremental upgrades over its predecessor rather than a dramatic redesign.\", \"The device is marginally heavier and thicker due to a switch from titanium to aluminum in its construction.\"]', 'https://photos5.appleinsider.com/gallery/62660-130016-renderashr-xl.jpg', 'N/A', 'Excellent, offering the best battery life in an iP', 'N/A'),
(79, 'vivo y36', 'vivo Y36', '₹14,999', '61/100', 'June 2023', 'Qualcomm Snapdragon 680 (6 nm)', 'Octa-core (4x2.4 GHz Kryo 265 Gold & 4x1.9 GHz Kryo 265 Silver)', '8GB', 'IPS LCD', '2388x1080 pixels (FHD+)', '90Hz', '6.64 inches', '50MP, f/1.8 (wide), PDAF', '2MP, f/2.4 (depth)', '2MP, f/2.4 (macro)', '16MP, f/2.5', '5000mAh', '44W FlashCharge', '128GB', 'Expandable via microSD (up to 1TB)', '[\"Attractive design and good build quality\", \"Long-lasting 5000mAh battery with 44W fast charging\", \"Decent main camera performance in good lighting conditions\"]', '[\"Underwhelming processor performance, not ideal for heavy gaming\", \"Lack of 5G connectivity (for the 4G model)\", \"Display brightness could be improved for outdoor visibility and lack of ultrawide camera\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A//static.beebom.com/wp-content/uploads/2023/06/Vivo-Y36-5G-smartphone-in-black-color-option-with-a-white-background-1.jpg%3Fw%3D640', '345,081 (v10)', 'Over a day of moderate usage, up to 1.5 days with ', '3.7/5'),
(81, 'samsung galaxy s20', 'Samsung Galaxy S20', '₹33,999', 'N/A', 'March 2020', 'Exynos 990', 'Octa Core', '8GB', 'Dynamic AMOLED 2X', '3200 x 1440 pixels (Quad HD+)', '120Hz', '6.2 inches', '12MP (wide, f/1.8)', '64MP (telephoto, f/2.0)', '12MP (ultrawide, f/2.2)', '10MP (f/2.2)', '4000 mAh', '25W Fast Charging', '128GB', 'UFS 3.0', '[\"Gorgeous 120Hz Dynamic AMOLED 2X display.\", \"Compact and ergonomic design for comfortable one-handed use.\", \"Versatile triple camera system with 8K video recording capabilities.\"]', '[\"Shorter battery life, significantly impacted by the 120Hz refresh rate.\", \"Absence of a 3.5mm headphone jack.\", \"Exynos variant (for India) may offer slightly inferior performance and battery efficiency compared to the Snapdragon variant.\"]', 'https://img.freepik.com/premium-photo/isolated-samsung-galaxy-s20-angled-view-displaying-curved-scree-white-background-clean_655090-799528.jpg', '664929 (v9)', '9 hours 31 minutes (60Hz) / 7 hours 45 minutes (12', '4/5'),
(83, 'samsung galaxy s21', 'Samsung Galaxy S21', '₹69,999', '86/100', 'January 2021', 'Exynos 2100', 'Octa-core (1x2.9 GHz Cortex-X1 & 3x2.80 GHz Cortex-A78 & 4x2.2 GHz Cortex-A55)', '8 GB', 'Dynamic AMOLED 2X', '1080 x 2400 pixels (FHD+)', '120Hz adaptive', '6.2 inches', '12 MP, f/1.8 (wide)', '64 MP, f/2.0 (telephoto)', '12 MP, f/2.2 (ultrawide)', '10 MP', '4000 mAh', '25W Fast Charging, 15W Wireless Charging, 4.5W Rev', '128 GB, 256 GB', 'UFS 3.1', '[\"Powerful performance\", \"Vibrant 120Hz Dynamic AMOLED 2X display\", \"Versatile camera system\"]', '[\"No microSD card slot for expandable storage\", \"Charger not included in the box\", \"Plastic (Glasstic) back design\"]', 'https://img.freepik.com/premium-photo/isolated-samsung-galaxy-s21-ultra-smartphone-front-view-showcasing-white-background-clean_655090-802099.jpg', '899,100 (v11)', 'Around 1.5 days (ViserMark Test Protocol)', '86/100'),
(85, 'samsung galaxy s23', 'Samsung Galaxy S23', '₹44,999', '92/100', 'February 2023', 'Qualcomm Snapdragon 8 Gen 2 for Galaxy', 'Octa-Core', '8 GB', 'Dynamic AMOLED 2X', '2340 x 1080 pixels (FHD+)', '120 Hz (Adaptive 48-120Hz)', '6.1 inches', '50 MP, f/1.8 (wide)', '12 MP, f/2.2 (ultrawide)', '10 MP, f/2.4 (telephoto)', '12 MP, f/2.2', '3900 mAh', '25W wired, Wireless Charging Supported', '128 GB', 'UFS 3.1', '[\"Powered by the highly efficient and powerful Snapdragon 8 Gen 2 for Galaxy processor.\", \"Features a compact and premium design with durable Gorilla Glass Victus 2 and an IP68 rating for dust and water resistance.\", \"Equipped with an excellent and versatile camera system that delivers impressive photos, including improved low-light capabilities, and a vibrant AMOLED display.\"]', '[\"Offers slower charging speeds (25W) compared to its larger S23 siblings and some competitors in the market.\", \"The rear camera hardware sees no major upgrades from its predecessor, with significant camera advancements primarily reserved for the S23 Ultra model.\", \"The base 128GB internal storage model utilizes the older UFS 3.1 technology, which is slower than the UFS 4.0 found in higher storage variants.\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A//static0.xdaimages.com/wordpress/wp-content/uploads/2023/01/phantom-black-galaxy-s23-on-white-background-leaked-marketing-image.jpg', '1,507,884 (v10)', 'Comfortably a full day (up to 13 hours 12 minutes ', '4/5'),
(86, 'samsung galaxy a73 5g', 'Samsung Galaxy A73 5G', '₹41,799', '80/100', 'March 2022', 'Qualcomm Snapdragon 778G 5G (6nm)', 'Octa-core (4x2.4 GHz Kryo 670 & 4x1.8 GHz Kryo 670)', '8GB', 'Super AMOLED Plus', '1080 x 2400 pixels (FHD+)', '120Hz', '6.7 inches', '108 MP, f/1.8, OIS', '12 MP, f/2.2 (ultrawide)', '5 MP, f/2.4 (macro)', '32 MP, f/2.2', '5000 mAh', '25W Fast Charging', '128GB/256GB', 'UFS', '[\"Beautiful and smooth 120Hz Super AMOLED Plus display\", \"Excellent, long-lasting battery life\", \"Snappy performance with Snapdragon 778G 5G\"]', '[\"Charger not included in the box\", \"No 3.5mm headphone jack\", \"Slower charging compared to some competitors\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A//i5.walmartimages.com/seo/Samsung-Galaxy-A73-5G-A736B-256GB-8GB-RAM-Dual-SIM-GSM-Unlocked-Awesome-White_8c567497-b980-459f-817d-9d6b8684f59f.b167a09135e8a9aa4665303bf533c946.jpeg%3FodnHeight%3D768%26o', '579,837 (v10)', 'Excellent, easily lasts a full day, up to two days', '4/5'),
(87, 'samsung galaxy s24 5g', 'Samsung Galaxy S24 5G', '₹40,999', '92/100', 'January 2024', 'Exynos 2400', 'Deca Core', '8 GB', 'Dynamic AMOLED 2X, LTPO', '2340 x 1080 pixels', '1-120 Hz adaptive', '6.2 inches', '50 MP', '12 MP (Ultra-Wide)', '10 MP (Telephoto, 3x Optical Zoom)', '12 MP', '4000 mAh', '25W wired, 15W wireless, 4.5W reverse wireless', '128 GB, 256 GB, 512 GB', 'UFS 3.1/4.0', '[\"Exceptional screen with high brightness\", \"Excellent battery life for a compact phone\", \"Seven years of OS and security updates\"]', '[\"Slower charging speeds compared to competitors\", \"Some Galaxy AI features are hit-or-miss\", \"Less RAM (8GB) than larger S24 models\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.smartprix.com/bytes/wp-content/uploads/2023/09/Samsung-Galaxy-S24-5K1-scaled.jpg', '2,011,752', '1.5 days (34 hours) or 13 hours 28 minutes of web ', '4.0/5'),
(88, 'techno pova 3', 'Tecno Pova 3', '₹6,999', '50/100', 'May 2022', 'MediaTek Helio G88 (12nm)', 'Octa-core (2x2.0 GHz Cortex-A75 & 6x1.8 GHz Cortex-A55)', '4GB, 6GB', 'IPS LCD', '1080x2460 pixels (FHD+)', '90 Hz', '6.9 inches', '50 MP', '2 MP (depth)', '2 MP (QVGA/unspecified)', '8 MP', '7000 mAh', '33W Fast Charging, 10W Reverse Charging', '64GB, 128GB', 'UFS 2.1', '[\"Massive 7000mAh battery.\", \"Large 6.9-inch 90Hz FHD+ display.\", \"Decent performance for the price (MediaTek Helio G88).\"]', '[\"No 5G connectivity.\", \"Cameras could be better.\", \"Bloatware present.\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A//d13pvy8xd75yde.cloudfront.net/global/phones/POVA3/pova3--yin.png', '264188 points', 'Over 9 hours under sustained load', 'N/A'),
(89, 'tecno pova 3', 'Tecno Pova 3', '₹6,999', 'N/A', 'May 2022', 'MediaTek Helio G88', 'Octa-core (2x 2.0 GHz Cortex-A75 & 6x 1.8 GHz Cortex-A55)', '4GB, 6GB', 'IPS LCD', '1080x2460 pixels (FHD+)', '90Hz', '6.9 inches', '50MP', '2MP (Macro)', '2MP (Depth)', '8MP', '7000mAh', '33W Flash Charge, 10W Reverse Charging', '64GB, 128GB', 'eMMC 5.1', '[\"Massive 7000 mAh battery with 33W fast charging.\", \"Large 6.9-inch 90Hz FHD+ display.\", \"Decent performance for daily tasks and gaming with MediaTek Helio G88.\"]', '[\"Camera performance could be better.\", \"Large size makes single-handed use difficult.\", \"No 5G connectivity.\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A//d13pvy8xd75yde.cloudfront.net/global/phones/POVA3/pova3--yin.png', '264,188 points (v10)', 'Excellent, up to 2 days with light usage', 'N/A'),
(90, 'techno pova', 'Tecno Pova', '₹10,449', '68/100', 'December 2020', 'MediaTek Helio G80', 'Octa-core (2x2.0 GHz Cortex-A75 & 6x1.8 GHz Cortex-A55)', '6GB', 'IPS LCD', '720x1640 pixels (HD+)', '60Hz', '6.8 inches', '16 MP (f/1.85)', '2 MP (macro)', '2 MP (depth)', '8 MP (f/2.0)', '6000 mAh', '18W Fast Charging', '128GB', 'eMMC', '[\"Huge 6000mAh battery with excellent battery life.\", \"Powerful MediaTek Helio G80 processor for gaming.\", \"Large 6.8-inch display for an immersive experience.\"]', '[\"720p HD+ display resolution is relatively low.\", \"Micro-USB charging port, which is outdated.\", \"Average camera performance compared to competitors at its launch.\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A//d13pvy8xd75yde.cloudfront.net/phones/lj8k/pova7%25E7%25B3%25BB%25E7%25B1%25BB800%25E5%259B%25BE/LJ9.png', '195498', 'Excellent, over 16 hours screen-on time', '3.5/5'),
(91, 'samsung s26', 'Samsung S26', '₹87,999', '85/100', '2024', 'Octa-Core Processor', '8 Cores', '8GB RAM', 'AMOLED Display', 'FHD+', '120Hz', '6.7 inches', '50MP Main Camera', '8MP Ultra-wide', '2MP Macro', '16MP Front', '5000mAh', '33W Fast Charging', '128GB', 'UFS 3.1', '[\"Good display quality\", \"Reliable battery life\", \"Smooth performance\"]', '[\"Average low-light camera\", \"No wireless charging\", \"Pre-installed bloatware\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F71JN2VbCqqL._AC_UF894%2C1000_QL80_.jpg&f=1&nofb=1', 'Approx. 600,000', '1.5 Days', '4.2/5'),
(92, 'nothing phone 4a', 'Nothing Phone 4A', '₹33,652', '85/100', '2024', 'Octa-Core Processor', '8 Cores', '8GB RAM', 'AMOLED Display', 'FHD+', '120Hz', '6.7 inches', '50MP Main Camera', '8MP Ultra-wide', '2MP Macro', '16MP Front', '5000mAh', '33W Fast Charging', '128GB', 'UFS 3.1', '[\"Good display quality\", \"Reliable battery life\", \"Smooth performance\"]', '[\"Average low-light camera\", \"No wireless charging\", \"Pre-installed bloatware\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.shopify.com%2Fs%2Ffiles%2F1%2F0586%2F3270%2F0077%2Ffiles%2FPhone-4a-Pro-White.png%3Fv%3D1772251228&f=1&nofb=1', 'Approx. 600,000', '1.5 Days', '4.2/5'),
(93, 'motorolo edge 70 fusion', 'Motorola Edge 70 Fusion', '₹25,999', '83/100', 'March 2026', 'Qualcomm Snapdragon 7s Gen 4', 'Octa-core', '8GB', 'Quad-curved AMOLED', '2772 x 1272 pixels (1.5K)', '144Hz', '6.78-inch', '50MP Sony LYTIA 710 (OIS)', '13MP Ultra-wide (with Macro)', 'N/A', '32MP', '7000mAh', '68W TurboPower', '128GB', 'UFS 3.1', '[\"Excellent battery life, often lasting up to two days with moderate use.\", \"Vibrant 144Hz quad-curved AMOLED display with high peak brightness.\", \"Slim and lightweight design with IP68 and IP69 dust and water resistance.\"]', '[\"Performance is reliable for everyday tasks but not ideal for heavy gaming.\", \"Cameras deliver good results in daylight but can struggle in low-light conditions.\", \"Software experience, while near-stock Android, includes some bloatware and occasional micro stutters.\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmotorolain.vtexassets.com%2Farquivos%2Fids%2F161666%2Fmotorola-edge-70-fusion-pdp-ecom-render-06-color5-4zlgawe8.png%3Fv%3D639072888087570000&f=1&nofb=1', '1,149,292 (v10)', 'Up to two full days with moderate usage, with a PC', '4.2/5'),
(94, 'samsung galaxy s25', 'Samsung Galaxy S25', '₹74,999', '91/100', 'February 2025', 'Qualcomm Snapdragon 8 Elite (3 nm)', 'Octa-core (2x4.47 GHz Oryon V2 Phoenix L + 6x3.53 GHz Oryon V2 Phoenix M)', '12 GB', 'Dynamic LTPO AMOLED 2X', '1080 x 2340 pixels (~416 ppi density)', '120 Hz', '6.2 inches', '50 MP, f/1.8 (wide), OIS, PDAF', '12 MP, f/2.2, 120˚ (ultrawide)', '10 MP, f/2.4 (telephoto), 3x optical zoom, OIS, PDAF', '12 MP, f/2.2 (wide), dual pixel PDAF', '4000 mAh', '25W wired, 15W wireless', '128GB/256GB/512GB', 'UFS 4.0', '[\"Compact size and premium design\", \"Powerful Snapdragon 8 Elite processor delivering top-tier performance\", \"Good camera system with enhanced AI features and 7 years of software support\"]', '[\"Iterative design with no significant changes from its predecessor\", \"Battery life is good for its size but shorter than larger models\", \"Camera lacks 5x optical zoom and some AI capabilities are considered overhyped\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F41-Bc14cmeL.jpg&f=1&nofb=1', '3,135,223 (v11)', 'Up to 37 hours of general use, with around 14-16 h', '4.55/5'),
(96, 'motorola edge 70 fusion', 'Motorola Edge 70 Fusion', '₹24,999', '87/100', 'March 2026', 'Qualcomm Snapdragon 7s Gen 4', '1x2.7 GHz Kryo + 3x2.4 GHz P•Cores + 4x1.6 GHz E•Cores (Octa-Core)', '8GB / 12GB LPDDR5X', '6.78-inch 1.5K Extreme AMOLED Quad Curved Display', '2772 x 1272 pixels', '144Hz', '6.78 inches', '50MP Sony LYTIA 710 sensor, OIS, f/1.8 aperture', '13MP ultra-wide with macro option, f/2.2 aperture', 'N/A', '32MP, f/2.2 aperture, 4K video recording', '7000mAh (Silicon-Carbon)', '68W TurboPower', '128GB / 256GB', 'UFS 3.1', '[\"Premium design with true quad-curved display.\", \"Excellent and long-lasting 7000mAh battery life.\", \"Vibrant 1.5K 144Hz AMOLED display.\"]', '[\"Average camera system performance.\", \"Software includes ads and slow update rollouts.\", \"Performance is not ideal for heavy gaming and the phone can warm up.\"]', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmotorolain.vtexassets.com%2Farquivos%2Fids%2F161666%2Fmotorola-edge-70-fusion-pdp-ecom-render-06-color5-4zlgawe8.png%3Fv%3D639072888087570000&f=1&nofb=1', '1,149,292', 'Up to 50 hours (with 7000mAh battery), easily 1-2 ', '4.5/5');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notification_preference`
--

CREATE TABLE `notification_preference` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `order_updates` tinyint(1) DEFAULT NULL,
  `warranty_alerts` tinyint(1) DEFAULT NULL,
  `ai_updates` tinyint(1) DEFAULT NULL,
  `promotions` tinyint(1) DEFAULT NULL,
  `frequency` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notification_preference`
--

INSERT INTO `notification_preference` (`id`, `user_id`, `order_updates`, `warranty_alerts`, `ai_updates`, `promotions`, `frequency`) VALUES
(1, 1, 1, 1, 1, 1, 'Daily summary'),
(2, 9, 1, 1, 1, 0, 'Daily summary');

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `order_date` datetime DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `invoice_no` varchar(20) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `tracking_number` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`id`, `user_id`, `product_id`, `order_date`, `status`, `invoice_no`, `payment_method`, `tracking_number`) VALUES
(56, 1, 730, '2026-03-24 09:14:21', 'Delivered', 'INV-3OR4TPLM', 'Cash On Delivery', NULL),
(57, 1, 740, '2026-03-24 14:36:18', 'Cancelled', 'INV-TFFWHGAH', 'Cash On Delivery', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `razorpay_order_id` varchar(100) DEFAULT NULL,
  `razorpay_signature` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`id`, `order_id`, `payment_method`, `amount`, `transaction_id`, `status`, `created_at`, `razorpay_order_id`, `razorpay_signature`) VALUES
(1, 3, 'Cash on Delivery', '150000.0', 'TXN-1FEC7685', 'Completed', '2026-02-20 04:16:44', NULL, NULL),
(2, 6, 'card', '1002499.0', 'TXN-66474229', 'Completed', '2026-02-20 07:44:33', NULL, NULL),
(3, 7, 'upi', '300000.0', 'TXN-E26D41EA', 'Completed', '2026-02-20 07:45:41', NULL, NULL),
(4, 8, 'card', '300000.0', 'TXN-9B91F796', 'Completed', '2026-02-20 07:52:31', NULL, NULL),
(5, 9, 'card', '300000.0', 'TXN-7FE232C3', 'Completed', '2026-02-20 07:54:16', NULL, NULL),
(6, 10, 'upi', '28999.0', 'TXN-3804E502', 'Completed', '2026-02-20 08:00:42', NULL, NULL),
(7, 12, 'upi', '59999.0', 'TXN-302ACE3A', 'Completed', '2026-02-20 08:17:21', NULL, NULL),
(8, 13, 'cod', '54999.0', 'TXN-A56D7111', 'Completed', '2026-02-20 08:33:06', NULL, NULL),
(9, 14, 'card', '52999.0', 'TXN-F793EF7C', 'Completed', '2026-02-20 08:45:55', NULL, NULL),
(10, 15, 'upi', '57999.0', 'TXN-2CDC6CB5', 'Completed', '2026-02-21 13:42:15', NULL, NULL),
(11, 16, 'card', '57999.0', 'TXN-C22114F0', 'Completed', '2026-02-21 13:45:39', NULL, NULL),
(12, 17, 'upi', '102498.0', 'TXN-F33C9250', 'Completed', '2026-02-23 07:14:01', NULL, NULL),
(13, 18, 'card', '15499.0', 'TXN-A9689ECF', 'Completed', '2026-02-23 07:27:06', NULL, NULL),
(14, 19, 'card', '30000.0', 'TXN-B0541C00', 'Completed', '2026-02-23 13:22:10', NULL, NULL),
(15, 20, 'card', '29999.0', 'TXN-27397B44', 'Completed', '2026-02-24 04:28:52', NULL, NULL),
(16, 21, 'card', '60000.0', 'TXN-9F7EA41E', 'Completed', '2026-02-24 05:18:14', NULL, NULL),
(17, 22, 'card', '59999.0', 'TXN-81C63A6E', 'Completed', '2026-02-24 07:23:07', NULL, NULL),
(18, 23, 'card', '89999.0', 'TXN-9F0F681E', 'Completed', '2026-02-25 13:07:51', NULL, NULL),
(19, 24, 'card', '29999.0', 'TXN-E1F721D5', 'Completed', '2026-02-25 13:28:53', NULL, NULL),
(20, 25, 'card', '26999.0', 'TXN-370AAA04', 'Completed', '2026-02-25 13:33:48', NULL, NULL),
(21, 26, 'card', '27999.0', 'TXN-4D468DAE', 'Completed', '2026-02-25 13:50:42', NULL, NULL),
(26, 32, 'card', '58998.0', 'TXN-FA016636', 'Completed', '2026-02-25 14:46:41', NULL, NULL),
(27, 33, 'card', '139999.0', 'TXN-C62215FE', 'Completed', '2026-02-26 04:44:29', NULL, NULL),
(28, 34, 'upi', '52999.0', 'TXN-B229193A', 'Completed', '2026-02-26 04:55:17', NULL, NULL),
(29, 35, 'upi', '12999.0', 'TXN-6E90C87D', 'Completed', '2026-02-26 09:31:49', NULL, NULL),
(30, 39, 'Razorpay', '38999.0', 'TXN-002CD794', 'Completed', '2026-02-27 07:17:52', NULL, NULL),
(31, 44, 'Razorpay', '26999.0', 'TXN-91CCF029', 'Completed', '2026-02-27 12:56:28', NULL, NULL),
(32, 1, 'Razorpay', '26999.0', 'TXN-E43F39EC', 'Completed', '2026-03-02 03:11:45', NULL, NULL),
(33, 2, 'Razorpay', '23999.0', 'TXN-2FEEE6FC', 'Completed', '2026-03-03 07:05:58', NULL, NULL),
(34, 1, 'Razorpay', '33999', 'pay_SN4G4q1gCwJk9c', 'Completed', '2026-03-04 07:33:49', 'order_SN4Fjy25gIfC3h', '5464746af7ab901a2e1ad2e49870e85babc26da19aa29ad927a914627c095470'),
(35, 1, 'Razorpay', '33999.0', 'TXN-E6DCB8E4', 'Completed', '2026-03-04 08:14:58', NULL, NULL),
(36, 1, 'Razorpay', '33999', 'pay_SN4yh4QotUjOHW', 'Completed', '2026-03-04 08:16:03', 'order_SN4yXXktY5wJLD', '89d94ae445cc51cdb73f6105107b8b951ca2f2862798df9a9b68ed9fe1a1bcb2'),
(37, 1, 'Razorpay', '33999', 'pay_SN5Fg2wM2D3p7C', 'Completed', '2026-03-04 08:32:08', 'order_SN5FWHPvEsB7wL', '589b85a7741d7f024da5ef7c18785abd95deed6be72f410b9dad1f6e46f6c1c2'),
(38, 2, 'Razorpay', '33999.0', 'TXN-9586F8A1', 'Completed', '2026-03-04 08:41:28', NULL, NULL),
(39, 3, 'Razorpay', '33999.0', 'TXN-2D3DD5C6', 'Completed', '2026-03-04 08:48:08', NULL, NULL),
(40, 4, 'Razorpay', '23999.0', 'TXN-69DADCD1', 'Completed', '2026-03-04 09:00:07', NULL, NULL),
(41, 1, 'Razorpay', '33999', 'pay_SNAySVywz8hJ9y', 'Completed', '2026-03-04 14:08:00', 'order_SNAyC05s4KiAXV', '438f4f1bc0333279ddad2474a8bb27fb182a4008f4bd18c0ae2877e091c8a3cb'),
(45, 13, 'Razorpay', '27200.0', 'TXN-F3A440D5', 'Successful', '2026-03-06 09:05:41', NULL, NULL),
(46, 14, 'Razorpay', '27999.0', 'TXN-373EACF8', 'Successful', '2026-03-06 16:35:56', NULL, NULL),
(47, 1, 'Razorpay', '29999', 'pay_SOExThfwZzE4EY', 'Successful', '2026-03-07 06:41:22', 'order_SOExDB1WA6vLC6', '6fea7aa54a7a33ff9a68023ed9818ce79f3a22db527a3a24a5190a7d3c220b25'),
(48, 15, 'Razorpay', '47998.0', 'TXN-9D829F08', 'Successful', '2026-03-07 06:45:16', NULL, NULL),
(49, 16, 'Razorpay', '47998.0', 'TXN-7C811110', 'Successful', '2026-03-07 07:24:23', NULL, NULL),
(50, 1, 'Razorpay', '99999', 'pay_SOgjjE6bJFydCr', 'Successful', '2026-03-08 09:51:46', 'order_SOgjTIHnj9lBn7', '6a9b8e373c9134e0ccfa9ac589488f02591063690013f00d4125711e497a5073'),
(51, 19, 'Razorpay', '99999.0', 'TXN-59067796', 'Successful', '2026-03-08 11:25:31', NULL, NULL),
(52, 1, 'Razorpay', '62874', 'pay_SOyghObHmeOgUU', 'Successful', '2026-03-09 03:25:21', 'order_SOygTjiWMlr4Ng', '3d01f7d47034fe16eb9ff7990bda48389c5ab8a00e9bd2809c8e85a8c4aa9a91'),
(53, 21, 'Razorpay', '96170.0', 'TXN-4206A178', 'Successful', '2026-03-09 03:28:32', NULL, NULL),
(54, 23, 'Cash on Delivery', '49999.0', 'TXN-A81DC918', 'Successful', '2026-03-09 07:45:42', NULL, NULL),
(55, 24, 'Razorpay', '55799.0', 'TXN-FD76ACF0', 'Successful', '2026-03-09 09:23:11', NULL, NULL),
(56, 1, 'Razorpay', '69999', 'pay_SPNihbsFDQntvq', 'Successful', '2026-03-10 03:54:34', 'order_SPNiV1lkqXuWiz', 'e52cf311139e797aa85c25c1595825062cc6a947fc2ab0df8557e336ca37bb68'),
(57, 1, 'Razorpay', '45999', 'pay_SPnd9UFCqcI51d', 'Successful', '2026-03-11 05:15:20', 'order_SPncpJKw6tbpxK', '483b1c1c9fe6a0342f3a3f0c94ec816f5c9015bd24754996c21ca2893d6a7ae0'),
(58, 1, 'Razorpay', '29999', 'pay_SPqPSLp8JGawJN', 'Successful', '2026-03-11 07:58:26', 'order_SPqPDvLIGF666l', '7da13922af5c39ff6f0b9d9ad1c315474f41354d582cf669f11c00081b76a87c'),
(59, 1, 'Razorpay', '42999', 'pay_SRkY1H5na6dGQq', 'Successful', '2026-03-16 03:32:29', 'order_SRkXi9fN64Oezs', '62d3e643801d81e0e0f8089828c75cbcbbfa35799e18c64157a6083d0f8097d4'),
(60, 30, 'Razorpay', '48875.0', 'TXN-380700FB', 'Successful', '2026-03-17 03:07:21', NULL, NULL),
(61, 31, 'Cash on Delivery', '33999.0', 'TXN-3453E1B6', 'Successful', '2026-03-17 03:09:26', NULL, NULL),
(62, 32, 'Cash on Delivery', '22999.0', 'TXN-E52F39FF', 'Successful', '2026-03-17 03:15:10', NULL, NULL),
(63, 33, 'Cash on Delivery', '33999.0', 'TXN-3C5CE850', 'Successful', '2026-03-17 04:05:26', NULL, NULL),
(64, 34, 'Cash on Delivery', '54999.0', 'TXN-68250F06', 'Successful', '2026-03-17 04:10:15', NULL, NULL),
(65, 35, 'Cash on Delivery', '22999.0', 'TXN-A913A686', 'Successful', '2026-03-17 04:26:15', NULL, NULL),
(66, 36, 'Cash on Delivery', '33999.0', 'TXN-8FFC5706', 'Successful', '2026-03-17 04:31:00', NULL, NULL),
(67, 1, 'Razorpay', '39995', 'pay_SSEr1Zay3VDMtl', 'Successful', '2026-03-17 09:11:16', 'order_SSEqiiIbg9F6Bp', 'f764d73b30600c567e2ac07b5a4bae2ca5278388db3294d5b0c6e10d271cc97c'),
(68, 42, 'Razorpay', '79999.0', 'TXN-DEC2D4F7', 'Successful', '2026-03-19 02:44:35', NULL, NULL),
(69, 1, 'Razorpay', '25000', 'pay_SSzMDwxXXFewfN', 'Successful', '2026-03-19 06:40:41', 'order_SSzLxfbTccCl6F', '5dfb46fad5029efa0e567a65dd24972a85f743a73e9551bcfd3ec2ed86bb9c8b'),
(70, 45, 'Razorpay', '10449.0', 'TXN-345FA482', 'Successful', '2026-03-23 04:36:00', NULL, NULL),
(71, 46, 'Razorpay', '10449.0', 'TXN-9B057242', 'Successful', '2026-03-23 04:44:46', NULL, NULL),
(72, 47, 'Cash on Delivery', '6999.0', 'TXN-B1DFD478', 'Successful', '2026-03-23 04:45:59', NULL, NULL),
(73, 50, 'Razorpay', '28998.0', 'TXN-5A1E3BA1', 'Successful', '2026-03-23 09:07:01', NULL, NULL),
(74, 51, 'Cash on Delivery', '25999.0', 'TXN-9F3C8908', 'Successful', '2026-03-23 09:15:18', NULL, NULL),
(75, 52, 'Razorpay', '30000.0', 'TXN-A1D5EDC1', 'Successful', '2026-03-24 02:55:50', NULL, NULL),
(76, 1, 'Razorpay', '31318', 'pay_SUuWpG7gxQ3xFx', 'Successful', '2026-03-24 03:15:20', 'order_SUuWeMXCMbDP1u', 'fba19ab896c5e2152894db16a46cdf96b6efe063dc33d0632c2d1de6f1d3848a'),
(77, 54, 'Cash on Delivery', '25051.0', 'TXN-43709ABA', 'Successful', '2026-03-24 03:17:58', NULL, NULL),
(78, 55, 'Cash on Delivery', '31318.0', 'TXN-1EE3534E', 'Successful', '2026-03-24 03:18:32', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `privacy_setting`
--

CREATE TABLE `privacy_setting` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `two_factor_auth` tinyint(1) DEFAULT NULL,
  `biometric_login` tinyint(1) DEFAULT NULL,
  `data_sharing` tinyint(1) DEFAULT NULL,
  `profile_visibility` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `privacy_setting`
--

INSERT INTO `privacy_setting` (`id`, `user_id`, `two_factor_auth`, `biometric_login`, `data_sharing`, `profile_visibility`) VALUES
(1, 1, 1, 0, 1, 'Public'),
(2, 3, 0, 0, 1, 'Public'),
(3, 9, 1, 1, 1, 'Public');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `price` varchar(50) DEFAULT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `battery_spec` varchar(100) DEFAULT NULL,
  `display_spec` varchar(100) DEFAULT NULL,
  `processor_spec` varchar(100) DEFAULT NULL,
  `camera_spec` varchar(100) DEFAULT NULL,
  `stock` int(11) DEFAULT 50,
  `category` varchar(100) DEFAULT 'Electronics'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `price`, `image_url`, `battery_spec`, `display_spec`, `processor_spec`, `camera_spec`, `stock`, `category`) VALUES
(1, 'Poco X6 Pro 5G', '₹27,999', 'https://s.yimg.com/fz/api/res/1.2/fbl6tkYQC19YvshxOOSXpA--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse3.mm.bing.net/th?q=Poco+X6+Pro+5G&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '5000mAh', '120Hz AMOLED', 'MediaTek Dimensity 8300-Ultra', '64MP OIS', 50, 'Electronics'),
(2, 'Samsung Galaxy S24+', '₹99,999', 'https://s.yimg.com/fz/api/res/1.2/kSRnc8aLxfHT0t2GT_h0QA--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse2.mm.bing.net/th?q=Samsung+S24+Plus&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '4900mAh', '6.7-inch Dynamic AMOLED 2X, 120Hz LTPO, QHD+', 'Exynos 2400', '50MP OIS Main, 12MP Ultrawide, 10MP Telephoto', 50, 'Electronics'),
(3, 'Redmi Note 13 Pro+ 5G', '₹29,999', 'https://s.yimg.com/fz/api/res/1.2/scLH.DGk_wscVjF46t.vjw--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse2.mm.bing.net/th?q=Redmi+Note+13+Pro+Plus+5G+Price&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '5000mAh', '120Hz 1.5K AMOLED', 'MediaTek Dimensity 7200 Ultra', '200MP OIS', 50, 'Electronics'),
(4, 'OnePlus 12', '69999', 'https://s.yimg.com/fz/api/res/1.2/kG.hjQs3EY5RYPV57yrqJQ--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse4.mm.bing.net/th?q=One+Plus+12&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '5400 mAh', 'LTPO AMOLED, 1B colors, Dolby Vision, HDR10+', 'Qualcomm Snapdragon 8 Gen 3', '50 MP, f/1.6, 23mm (wide), 1/1.43\", 1.12µm, multi-directional PDAF, OIS (Sony LYT-808)', 50, 'Electronics'),
(5, 'POCO X6 Pro 5G (8GB/256GB)', '₹27,999', 'https://s.yimg.com/fz/api/res/1.2/QLg8T_c5vnDU9kZJVnhbcA--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse3.mm.bing.net/th?q=Poco+Phone+X6+Pro&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '5000mAh', '120Hz AMOLED', 'MediaTek Dimensity 8300-Ultra', '64MP OIS', 50, 'Electronics'),
(6, 'iQOO 12 5G', '₹57,999', 'https://s.yimg.com/fz/api/res/1.2/gtEZdG3Z3_w4JrUsss7QFQ--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse2.mm.bing.net/th?q=Iqoo+5&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '5000mAh', '144Hz LTPO AMOLED', 'Snapdragon 8 Gen 3', '50MP (OIS) Main', 50, 'Electronics'),
(7, 'Samsung Galaxy S23 5G', '₹56,999', 'https://s.yimg.com/fz/api/res/1.2/w70YNQ5a59kD9FAJNdrdYw--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse1.mm.bing.net/th?q=Samsung+Galaxy+S23+128GB&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '3900mAh', '120Hz Dynamic AMOLED 2X', 'Snapdragon 8 Gen 2 for Galaxy', '50MP', 50, 'Electronics'),
(8, 'Vivo V29e', '₹28,999', 'https://s.yimg.com/fz/api/res/1.2/EbSyddUQhPZh8wQNGx26kw--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse2.mm.bing.net/th?q=Vivo+V29e+Pro&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '5000mAh', '120Hz AMOLED', 'Snapdragon 695', '64MP OIS', 50, 'Electronics'),
(9, 'OPPO Reno11 5G', '₹29,999', 'https://s.yimg.com/fz/api/res/1.2/KZWP7QnosYxkTZZndpsKjQ--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse2.mm.bing.net/th?q=Oppo+Reno+11+Pro+Plus&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '4800mAh', '120Hz AMOLED', 'MediaTek Dimensity 7050', '50MP OIS Triple Camera', 50, 'Electronics'),
(10, 'Redmi Note 13 Pro 5G', '₹27,999', 'https://s.yimg.com/fz/api/res/1.2/9nj5K4M483iAiYKD1kAv3w--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD05Njt3PTk2/https://tse4.mm.bing.net/th?q=Redmi+Note+13+Pro+Green&pid=Api&mkt=en-US&cc=US&setlang=en&adlt=strict&t=1', '5100mAh', '120Hz AMOLED', 'Snapdragon 7s Gen 2', '200MP OIS', 50, 'Electronics'),
(11, 'POCO X6 Pro 5G (8GB RAM, 256GB Storage)', '21999', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTtwb-FBVZQJBNjD-YD9E-4cPkyC73txkc3Sx7Klxg1KXOdU2GILWGsjAtu3vxygRnXbbqrMiHz9U3NXFx2l_kcOdCO9bmRjmkv1lbvWfmH&usqp=CAc', '5000mAh with 67W fast charging', '6.67\" 1.5K AMOLED 120Hz', 'MediaTek Dimensity 8300-Ultra', '64MP OIS Main', 50, 'Electronics'),
(16, 'OnePlus Nord CE 4 5G', '₹26,999', 'https://www.mobiledokan.com/media/oneplus-nord-4-mercurial-silver-official-image_2.webp', '5500mAh', '120Hz', 'Snapdragon 7 Gen 3', '50MP', 50, 'Electronics'),
(43, 'OnePlus Nord 3 5G (8GB RAM, 128GB Storage)', '29999', 'https://images.unsplash.com/photo-1678911820864-e2c567c655d7?q=80&w=600', '5000mAh with 80W SuperVOOC charging', '6.74-inch AMOLED, 1.5K resolution, 120Hz refresh rate', 'MediaTek Dimensity 9000 5G', '50MP main (Sony IMX890 with OIS), 8MP ultrawide, 2MP macro', 50, 'Electronics'),
(44, 'Samsung Galaxy A35 5G (8GB RAM, 128GB Storage)', '28999', 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?q=80&w=600', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(45, 'Nothing Phone (2a) (8GB RAM, 128GB Storage)', '23999', 'https://m.media-amazon.com/images/I/618TOqXk+bL.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(64, 'OnePlus 12R (256GB)', '45999', 'https://images.unsplash.com/photo-1678911820864-e2c567c655d7?q=80&w=600', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(71, 'Samsung Galaxy S25', '74999', 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?q=80&w=600', '4000 mAh', 'Dynamic LTPO AMOLED 2X', 'Qualcomm Snapdragon 8 Elite (3 nm)', '50 MP, f/1.8 (wide), OIS, PDAF', 50, 'Electronics'),
(73, 'Samsung Galaxy S25 Ultra 256Gb', '109490', 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?q=80&w=600', '5000 mAh', 'Dynamic LTPO AMOLED 2X', 'Snapdragon 8 Elite for Galaxy', '200MP f/1.7 (Wide)', 50, 'Electronics'),
(79, 'Oneplus Nord 2T Size', '24490', 'https://sm.pcmag.com/t/pcmag_me/review/o/oneplus-13/oneplus-13_kd8t.1200.jpg', '4500mAh', 'AMOLED', 'MediaTek Dimensity 1300', '50MP (Sony IMX766) with OIS', 50, 'Electronics'),
(146, 'OnePlus 12R (16GB RAM, 256GB Storage)', '49999', 'https://sm.pcmag.com/t/pcmag_me/review/o/oneplus-13/oneplus-13_kd8t.1200.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(152, 'Samsung Galaxy S25 Ultra', '109490', 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?q=80&w=600', '5000mAh', 'Dynamic AMOLED 2X', 'Qualcomm Snapdragon 8 Elite for Galaxy', '200MP Wide Angle', 50, 'Electronics'),
(155, 'Oneplus 13', '69999', 'https://sm.pcmag.com/t/pcmag_me/review/o/oneplus-13/oneplus-13_kd8t.1200.jpg', '6000mAh', 'LTPO AMOLED', 'Qualcomm Snapdragon 8 Elite', '50MP Sony LYT-808, f/1.6, OIS', 50, 'Electronics'),
(156, 'Oneplus 15', '72999', 'https://sm.pcmag.com/t/pcmag_me/review/o/oneplus-13/oneplus-13_kd8t.1200.jpg', '7300 mAh', 'LTPO AMOLED', 'Qualcomm Snapdragon 8 Elite Gen 5', '50 MP (Sony IMX906/LYT-700) with OIS', 50, 'Electronics'),
(175, 'Samsung Galaxy S23 Ultra (256GB)', '104999', 'https://wsrv.nl/?url=https%3A//www.techlusive.in/wp-content/uploads/2023/12/Samsung-Galaxy-S23-Ultra-deal-7.jpg&w=600&output=webp', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(176, 'Samsung Galaxy S24 (256GB)', '85999', 'https://wsrv.nl/?url=http%3A//rukmini1.flixcart.com/image/300/300/xif0q/mobile/f/n/u/-original-imagx9egm9mgmvab.jpeg&w=600&output=webp', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(183, 'Oneplus Nord Ce3 5G', '26999', 'https://wsrv.nl/?url=https%3A//rukminim2.flixcart.com/image/416/416/xif0q/mobile/l/7/k/-original-imagtxvur9yrxvru.jpeg%3Fq%3D70&w=600&output=webp', '5000 mAh', 'Fluid AMOLED', 'Qualcomm Snapdragon 782G', '50MP Sony IMX890 (f/1.8, OIS)', 50, 'Electronics'),
(187, 'Iphone 16 Pro', '119900', 'https://wsrv.nl/?url=https%3A//static.digit.in/iPhone-16-Pro-.png&w=600&output=webp', '3582 mAh', 'Super Retina XDR OLED with ProMotion', 'Apple A18 Pro', '48MP (f/1.78, 24mm, second-generation sensor-shift OIS)', 50, 'Electronics'),
(188, 'Iphone 15 Pro', '89994', 'https://wsrv.nl/?url=https%3A//m.media-amazon.com/images/I/81fO2C9cYjL._AC_UL800_QL65_.jpg&w=600&output=webp', '3,274 mAh', 'LTPO Super Retina XDR OLED', 'Apple A17 Pro (3 nm)', '48MP Main (ƒ/1.78, sensor-shift OIS)', 50, 'Electronics'),
(193, 'iPhone 13 Pro', '119900', 'https://wsrv.nl/?url=https%3A//m.media-amazon.com/images/I/61nEaHtArzL._AC_UL960_QL65_.jpg&w=600&output=webp', '3095 mAh', 'Super Retina XDR OLED with ProMotion', 'Apple A15 Bionic', '12MP Wide (f/1.5, sensor-shift OIS)', 50, 'Electronics'),
(194, 'Motorola Moto G54 5G (8GB RAM, 128GB Storage)', '14999', 'https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928-u1.jpg', '6000mAh', '6.5-inch FHD+ 120Hz LCD', 'MediaTek Dimensity 7020', '50MP', 50, 'Electronics'),
(196, 'Vivo Y28 5G (4GB RAM, 128GB Storage)', '13999', 'https://fdn2.gsmarena.com/vv/bigpic/vivo-x100-pro.jpg', '5000mAh', '90Hz LCD', 'MediaTek Dimensity 6020', '50MP Dual Camera', 50, 'Electronics'),
(197, 'Vivo T2x 5G (4GB RAM, 128GB Storage)', '12999', 'https://fdn2.gsmarena.com/vv/bigpic/vivo-x100-pro.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(198, 'OnePlus 11 5G', '49999', 'https://wsrv.nl/?url=https%3A//m.media-amazon.com/images/I/61YexRaP2aL._SL1200_.jpg&w=600&output=webp', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(199, 'OnePlus Nord CE 4', '26999', 'https://wsrv.nl/?url=https%3A//fdn2.gsmarena.com/vv/pics/oneplus/oneplus-nord-ce3-5g-3.jpg&w=600&output=webp', '5500mAh (100W SuperVOOC)', '6.7-inch Fluid AMOLED, 120Hz', 'Qualcomm Snapdragon 7 Gen 3', '50MP Sony LYT-600 (OIS)', 50, 'Electronics'),
(200, 'POCO F5', '25999', 'https://wsrv.nl/?url=https%3A//fdn2.gsmarena.com/vv/bigpic/xiaomi-poco-f5-2.jpg&w=600&output=webp', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(201, 'Xiaomi 14', '59999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfBPIKEii5ScUNUveFHSHq6xFSPD-Xm5RCod_hhWe8WZFzGCtH8efQxcH_pTE&s', '4610mAh', '6.36-inch LTPO AMOLED, 120Hz', 'Qualcomm Snapdragon 8 Gen 3', '50MP', 50, 'Electronics'),
(206, 'Iphone 15 Pro Max', '159900', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQNwAFQHqnB2PPLzqzuZSSbJwb2H94sjH_aQuqlbgCXos4XcJmIVB15nmo7w&s', '4422 mAh', 'Super Retina XDR OLED', 'Apple A17 Pro', '48MP, f/1.78, second-generation sensor-shift OIS', 50, 'Electronics'),
(211, 'Iphone 16 Pro Max', '134900', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc5IHjyqZl8n_HWNlFc0VvpCxpSVwZ70enu4PPTseo-4XGwRhVGyeFyDSaQUc&s', '4685 mAh', 'Super Retina XDR OLED', 'Apple A18 Pro chip', '48 MP Wide Angle Primary Camera, ƒ/1.78 aperture, second-generation sensor-shift optical image stabi', 50, 'Electronics'),
(214, 'Poco X6 Neo (8GB RAM, 128GB Storage)', '14999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxoGA_28q1FsCLBrzTwY17O4giYo9ztLWdrg-H9nRggCTsFjfVbWY_xfiG1A&s', '5000mAh', '6.67-inch AMOLED, 120Hz', 'MediaTek Dimensity 6080', '108MP + 2MP Dual Rear, 16MP Front', 50, 'Electronics'),
(215, 'Poco M6 Pro 5G (8GB RAM, 256GB Storage)', '14999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7XK6FUKhuiXi8f3zzh7VBrALl_4YOHzBT9oVTBKOamXMdxCBOyKiq17DxKwA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(216, 'Poco M6 Pro 5G (6GB RAM, 128GB Storage)', '12999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7XK6FUKhuiXi8f3zzh7VBrALl_4YOHzBT9oVTBKOamXMdxCBOyKiq17DxKwA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(217, 'Xiaomi 14 (12GB RAM, 512GB Storage)', '59999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfBPIKEii5ScUNUveFHSHq6xFSPD-Xm5RCod_hhWe8WZFzGCtH8efQxcH_pTE&s', '4610mAh', '6.36-inch 120Hz LTPO AMOLED', 'Qualcomm Snapdragon 8 Gen 3', '50MP + 50MP + 50MP Triple Rear (Leica optics)', 50, 'Electronics'),
(218, 'iQOO 12 5G (12GB RAM, 256GB Storage)', '54999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkGj0PfME1NzznysanU5V4WoQm-chA3fZAP6I4Xeo_ns-RbRFDO1y46W-ePQ&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(219, 'Nothing Phone 2 (12GB RAM, 256GB Storage)', '38999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmTFiIrFhybgLD6DEIR4u88Z342n1-SRYquhSV1PaeNYKbVTbGNjf38xaTgg&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(220, 'POCO X6 Pro 5G (12GB RAM, 512GB Storage)', '25999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRb-ZhLXdCggVkLIXr25WuTMJ7O0fn93JQUJapaSu0nd07yTBJyZf1wOsDGSg&s', '5000mAh with 67W Turbo Charging', '6.67-inch 1.5K Flow AMOLED, 120Hz Refresh Rate', 'MediaTek Dimensity 8300-Ultra', '64MP OIS Triple Rear Camera, 16MP Front Camera', 50, 'Electronics'),
(221, 'Realme 12 Pro+ 5G (12GB RAM, 256GB Storage)', '23999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpRsQOlctxdFf4HrEtDsmo7kVzWEXRbmR0_lGTXrXj-mljNp35GFbypZgBm8c&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(222, 'Redmi Note 13 Pro+ 5G (12GB RAM, 256GB Storage)', '26999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmp9GHI5I0m-Mn8eE4KLmQr7BpG8hhnOnGWy78hrAefg23DUMZcIWeKDX5gA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(230, 'POCO X6 Pro 5G (Racing Grey, 512 GB) (12 GB RAM)', '28999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSup36AkZiiFm1ekEukdMOX6Aon4KIvs_Oxsh4RyIvJAuqhmRtI02kfNbq1oA&s', '5000mAh', '6.67 inches OLED, 120Hz', 'MediaTek Dimensity 8300-Ultra', '64MP Triple', 50, 'Electronics'),
(231, 'realme 12 Pro+ 5G (Submarine Blue, 256 GB) (12 GB RAM)', '29999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpRsQOlctxdFf4HrEtDsmo7kVzWEXRbmR0_lGTXrXj-mljNp35GFbypZgBm8c&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(232, 'Redmi Note 13 Pro+ 5G (Fusion Black, 256 GB) (8 GB RAM)', '24999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmp9GHI5I0m-Mn8eE4KLmQr7BpG8hhnOnGWy78hrAefg23DUMZcIWeKDX5gA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(233, 'Realme 12 Pro+ 5G (8GB RAM, 256GB Storage)', '22999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpRsQOlctxdFf4HrEtDsmo7kVzWEXRbmR0_lGTXrXj-mljNp35GFbypZgBm8c&s', '5000mAh', '6.7-inch AMOLED 120Hz', 'Qualcomm Snapdragon 7s Gen 2', '64MP Periscope + 50MP OIS + 8MP Rear, 32MP Front', 50, 'Electronics'),
(234, 'OnePlus Nord CE 4 5G (8GB RAM, 256GB Storage)', '22670', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTek1D_NhEV_sYuCvsP4nlv3KDRvZU7ZG-DR6zeufjLlLfk-AA4pITkQ_pUGw&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(235, 'Redmi Note 13 Pro+ 5G (8GB RAM, 256GB Storage)', '24999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmp9GHI5I0m-Mn8eE4KLmQr7BpG8hhnOnGWy78hrAefg23DUMZcIWeKDX5gA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(281, 'Apple Iphone 16 Pro Max 256 Gb', '132900', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkjWIY9yKUP6j2fLJ3UNE5hJN1mzmRQyEfCo8HO_igkh3vK3OMnFkmr5UDmg&s', '4685 mAh', 'LTPO Super Retina XDR OLED', 'Apple A18 Pro chip', '48 MP, f/1.78 (wide)', 50, 'Electronics'),
(295, 'Apple Iphone 16 Pro Max', '134900', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkjWIY9yKUP6j2fLJ3UNE5hJN1mzmRQyEfCo8HO_igkh3vK3OMnFkmr5UDmg&s', '4685 mAh', 'Super Retina XDR OLED', 'A18 Pro chip (New 6-core CPU with 2 performance and 4 efficiency cores, New 6-core GPU, New 16-core ', '48 MP Wide Angle', 50, 'Electronics'),
(304, 'OnePlus Nord 5', '32499', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_-fxq-LuHdZM9YqS6TSIDEeDUFUlk-NxN-fYm0N5Py4phC5TJGPe8fVtU5RE&s', '6800mAh | 80W Fast Charging', '6.83\" 144Hz Swift AMOLED', 'Snapdragon 8s Gen 3', '50MP + 8MP Rear | 50MP Front', 50, 'Electronics'),
(305, 'Realme 16 Pro', '34999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBfWkOYKGsgu7iQBSEYURBDPXwnzGbPetx_vLTgcBw79mWHo359fGLkfFddQ&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(306, 'Motorola Edge 70', '29948', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7Oo7Rov8F9vw6fKtaKf3wHHXOby2rWWRIlpd0QALCYaEi-w8edBnIv1ckmw&s', '5000mAh', 'P-OLED', 'Qualcomm Snapdragon 7 Gen 4 SoC', '50MP, f/1.8 with PDAF, OIS', 50, 'Electronics'),
(309, 'MOTOROLA Edge 60 Pro (8GB RAM, 256GB Storage)', '27838', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpodg1oDRYMa_uorlq6fLbVQZabT-gvh2KmVs1-8lJK05RLs5VASEKbnkSug&s', '6000mAh | 90W Turbo Power Charging', '6.7-inch P-OLED | 120Hz Refresh Rate | Super HD (1220p)', 'MediaTek Dimensity 8350 Extreme', '50MP (Main, OIS) + 50MP (Ultrawide) + 10MP (Telephoto, 3x Optical Zoom, OIS) Rear | 50MP Front', 50, 'Electronics'),
(310, 'realme P4 Power 5G (8GB RAM, 128GB Storage)', '24615', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2Zgeyk_J27Whj2X-g4FTdSmhTEromZysAYVW6YGk3L5CacoSor23Ic0QtKw&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(311, 'OnePlus Nord CE 5 5G (8GB RAM, 128GB Storage)', '24998', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoZ6hrsHmmer-XB6xWHFAgqcVToC9Q4J1xI7qYL_BtseIGMS7fYLd0HeLqDQ&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(313, 'Redmi K50i 5G (8GB RAM, 256GB Storage)', '21999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-a7yBaXq8a97jANDsyLOcqFoPAm2O5hRhtuaRE8_-U7p-qqYKxc2SJgeLcw&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(314, 'Samsung Galaxy A55 5G (8GB RAM, 256GB)', '27999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRZBsV84MWNf7YGi_NmIfzlaP5fAjL0O-Pemv_NSbCalN20SUFlW0l9wOipiE&s', '5000mAh', '6.6-inch Super AMOLED, 120Hz', 'Exynos 1480', '50MP (OIS) + 12MP + 5MP', 50, 'Electronics'),
(315, 'Redmi Note 13 Pro+ 5G (8GB RAM, 256GB)', '24999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmp9GHI5I0m-Mn8eE4KLmQr7BpG8hhnOnGWy78hrAefg23DUMZcIWeKDX5gA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(317, 'iQOO Neo 7 Pro (12GB RAM, 256GB Storage)', '35999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHl20vnfUl6MxlMOPzZ2_WbPxGiPzt0CZrPHRS3J_WTNfov-9EfweoaxqSqhg&s', '5000mAh', '6.78-inch 120Hz AMOLED', 'Qualcomm Snapdragon 8+ Gen 1', '50MP', 50, 'Electronics'),
(319, 'OnePlus Nord 3 5G (8GB RAM, 256GB Storage)', '26949', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHKHk-SesC4Q7x9jUVGdSWsS4TJ-Z84YMuT4rYieo8NC2E673vPM4JXwS7PA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(320, 'OnePlus Nord 3 5G (16GB RAM, 256GB Storage)', '27990', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHKHk-SesC4Q7x9jUVGdSWsS4TJ-Z84YMuT4rYieo8NC2E673vPM4JXwS7PA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(321, 'iQOO Neo 9 Pro 5G (8GB RAM, 256GB Storage)', '33999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmM_boyHYhdbCWOZsIzqS4mGXxBAoa6Tz5uM9XiLwVv1z1Ggtp2uZQLw1QLeE&s', '5160mAh', '6.78-inch 1.5K LTPO AMOLED, 144Hz', 'Snapdragon 8 Gen 2', '50MP + 8MP', 50, 'Electronics'),
(322, 'Samsung Galaxy S25 256Gb Unlocked', '74999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4k0heIzAdnLz5mjeqa1i5uR1JLJH2znUxOxHpA-BJlMEZC1X_zR_uqwGiCB8&s', '4000 mAh', 'Dynamic LTPO AMOLED 2X', 'Qualcomm Snapdragon 8 Elite for Galaxy', '50 MP (wide)', 50, 'Electronics'),
(345, 'Samsung Galaxy A55 5G (12GB RAM, 256GB Storage)', '29999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRZBsV84MWNf7YGi_NmIfzlaP5fAjL0O-Pemv_NSbCalN20SUFlW0l9wOipiE&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(346, 'Samsung Galaxy M55 5G (12GB RAM, 256GB Storage)', '22998', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLcF03KpXKZ8ua7upVRktjLbZ_jaYKRbI3Cp8i4whW7XseWkoTq2XccT5huAE&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(347, 'iQOO Neo 7 Pro 5G (8GB RAM, 128GB Storage)', '29999', 'https://m.media-amazon.com/images/I/712pLRfzDYL.jpg', '5000mAh, 120W Fast Charging', '6.78-inch AMOLED, 120Hz Refresh Rate', 'Qualcomm Snapdragon 8+ Gen 1', '50MP + 8MP + 2MP Triple Rear, 16MP Front', 50, 'Electronics'),
(348, 'POCO F5 (8GB RAM, 256GB Storage)', '29999', 'https://m.media-amazon.com/images/I/61xunOpkIrL._AC_UF1000,1000_QL80_.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(351, 'iQOO Neo 9 Pro 5G (12GB RAM, 256GB Storage)', '33999', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcS18KfLoAjnNExJoDMMnsIoVXEvUy_Ts_Ni-9yhQDS-I6k7P_dvRDqfSTBuMM9hbBBMs64EWXX3izWavZbJ5XNvay5B2O1HlOPY4MToY2O_V8VFvfDFwGeo276J6DTIdg&usqp=CAc', '5160mAh', '144Hz LTPO AMOLED', 'Qualcomm Snapdragon 8 Gen 2', '50MP', 50, 'Electronics'),
(353, 'Realme GT 6T 5G (12GB RAM, 256GB Storage)', '29999', 'https://m-cdn.phonearena.com/images/phones/85257-350/Realme-12-Pro-Plus.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(354, 'iQOO Neo 10R (8GB RAM, 128GB)', '26999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9BnAZYbF_JxWakE689d9Ie8Jxjj2UABwhkNp-NJRaQTGYpkdg2waO_KhhCg&s', '6400mAh', '144Hz AMOLED', 'Snapdragon 8s Gen 3', '50MP', 50, 'Electronics'),
(355, 'Motorola Edge 60 Pro (8GB RAM, 256GB)', '27989', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpodg1oDRYMa_uorlq6fLbVQZabT-gvh2KmVs1-8lJK05RLs5VASEKbnkSug&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(356, 'Xiaomi Redmi Note 15 Pro (8GB RAM, 128GB)', '29999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeCsagJhZkK_Nm6IiddsyI1KBrS1oKzKuC_yoN7zYyI5UfDRHecHEMnhFmUbM&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(357, 'Realme GT 6T (12GB RAM, 512GB Storage)', '30999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIzxp_SglTgNfYal03BQaEAXvIZdiRbQ14zQwkdrCSwzGN9wRRfTo8fUQ8PQ&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(371, 'Samsung Galaxy S25 5G', '74999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQX0Ju8kz5vRm1YuHf0w5KSvMECJMqM0m4_0ry3CGoBZ6VgTzxMdUMGudIzho&s', '4000 mAh', '6.2 inches (15.75 cm); Dynamic AMOLED 2x', 'Qualcomm Snapdragon 8 Elite', 'Triple Camera Setup 50 MP Wide Angle Primary Camera 12 MP Ultra-Wide Angle Camera 10 MP Telephoto (u', 50, 'Electronics'),
(372, 'Poco F5 5G (12GB RAM, 256GB Storage)', '33999', 'https://www.91-img.com/pictures/173257-v4-vivo-v70-mobile-phone-hres-1.jpg?tr=h-630,q-70', '5000mAh with 67W Fast Charging', '6.67-inch AMOLED, 120Hz refresh rate', 'Qualcomm Snapdragon 7+ Gen 2', '64MP (main) + 8MP (ultrawide) + 2MP (macro) Triple Rear Camera', 40, 'Electronics'),
(373, 'Vivo V70', '29999', 'https://www.91-img.com/pictures/173257-v4-vivo-v70-mobile-phone-hres-1.jpg?tr=h-630,q-70', '5000mAh', 'AMOLED Display', 'Octa-Core Processor', '50MP Main', 35, 'Smartphone'),
(374, 'iQOO Neo 10R (8GB RAM, 256GB)', '28999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9BnAZYbF_JxWakE689d9Ie8Jxjj2UABwhkNp-NJRaQTGYpkdg2waO_KhhCg&s', '6400mAh', '6.78-inch AMOLED, 144Hz', 'Qualcomm Snapdragon 8s Gen 3', '50MP', 50, 'Electronics'),
(375, 'Redmi Note 15 Pro 5G (8GB RAM, 128GB)', '29299', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUUqUObZKtvJT1Sz1IZHfcS3AL2E_MWJC9V_fb0MsAKAjkROQMjTLJkpNlsQ&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(392, 'Samsung Galaxy A73 5G', '41799', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmOQlQPQ3Ge-YCUDEhSc36OoRSO6bRHxXGh1_fg8Z8n3qeUMxgWuvE2hpzYA&s', '5000 mAh', 'Super AMOLED Plus', 'Qualcomm Snapdragon 778G 5G (6nm)', '108 MP, f/1.8, OIS', 50, 'Electronics'),
(405, 'Samsung Galaxy S26', '87999', 'https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s26.jpg', '4300 mAh', 'Dynamic LTPO AMOLED 2X', 'Qualcomm Snapdragon 8 Elite Gen 5 / Samsung Exynos 2600', '50MP (f/1.8 aperture, 1/1.56-inch sensor size, Dual Pixel PDAF, OIS)', 50, 'Electronics'),
(410, 'iQOO 12 (12GB RAM, 256GB)', '48875', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQxdcb3LBYzQpSr3WSAtftqzpDqc9FF5mQ5DDOslxTGWynUZNQWA9Ofw06xfiZKUH9-HkGGLr_FDQatwlFrPU-Uk-aS9QWaf6JcY69zHki_elH3wSAVP5ekwPT0ugilzAqAfCX7qtnIXZE&usqp=CAc', '5000mAh with 120W Fast Charging', '6.78-inch 144Hz AMOLED', 'Snapdragon 8 Gen 3', '50MP + 64MP + 50MP Triple Rear', 50, 'Electronics'),
(411, 'OnePlus 12 (12GB RAM, 256GB)', '54884', 'https://m.media-amazon.com/images/I/717Qo4MH97L._SX679_.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(413, 'Google Pixel 8 (8GB RAM, 128GB)', '36999', 'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQTP7lwfvtnnuQpQ1HD0jK1OEtusGG0mosVfnPauLejcWp-8YiV_n-sA04OFQeqlTuV0vu1vmjWM03hoGQjMGyVAH9Bq1wCCI8f0ahKd1StfFpTbqrD8R1ZzzKwbplbUCLBPOZL6Sc&usqp=CAc', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(430, 'Samsung Galaxy S25 Plus', '74999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSReevz2s5RJbeDGx5amLWeMioOqq26bhBsDGphxICx5xnaWABRigQADbT8jGM&s', '4900 mAh', 'Dynamic AMOLED 2X', 'Qualcomm Snapdragon 8 Elite', '50 MP', 50, 'Electronics'),
(431, 'Samsung Galaxy S22', '72999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcPFQSebzXeFd7FL4d2J0WGSfh0Vy72qrOJY1NUe_NBeAtA2TbzfPMAmzIxPQ&s', '3700 mAh', 'Dynamic AMOLED 2X', 'Qualcomm Snapdragon 8 Gen 1 / Samsung Exynos 2200', '50 MP, f/1.8, OIS (wide)', 50, 'Electronics'),
(443, 'Motorola Edge 50 Fusion', '18999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2yoag3j86ZFcHI57LN6b1GsJyVGtFSHs-ZEdU9sW9bZVPB72tZXyma89OREA&s', '5000 mAh', 'P-OLED', 'Qualcomm Snapdragon 7s Gen 2', '50MP (Sony Lytia 700C, f/1.8, OIS)', 50, 'Electronics'),
(455, 'Xiaomi Redmi Note 8 Pro', '9490', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOTggr67xmyeGNCPBDlhTvfSUjSKdOp1FOiIFfXyMpHQrn_nIVeGCMjZdsJCc&s', '4500 mAh', 'IPS LCD', 'MediaTek Helio G90T', '64MP', 50, 'Electronics'),
(456, 'Redmi Note 9 Pro', '11499', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZ8AqHqh_n9sE5CDF1NCyGl66A4kjLeFgtUx4T6LLrsh0RGfRR-bVJ--9Uv2Y&s', '5020mAh', 'IPS LCD', 'Qualcomm Snapdragon 720G', '48MP', 50, 'Electronics'),
(459, 'Iphone 17 5G 256Gb Sage', '78900', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbjwqKr-uQOd7LNTQdB8cZi5cTId-y4fzeOcgyoF61mKA373mS36o2M3feVw&s', '3692 mAh', 'Super Retina XDR OLED with ProMotion', 'Apple A19 Chip', '48MP Fusion Main (f/1.6, sensor-shift OIS, 2x optical-quality telephoto enabled)', 50, 'Electronics'),
(461, 'OnePlus Nord CE 4 5G (8GB RAM, 128GB Storage)', '22598', 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQZ2W-BnwhfkGSMdkPoqoVASVILqqlUeRx5sRjSOLNEtzo7PnR9OaCfAsKS6sMHyruTu7_qkdzyNMt9QpGRvTcbPNDTOhvyWptIaZELEbsxCVEF2o4Foex2pg&usqp=CAc\n', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(462, 'Oppo Reno 11 5G (8GB RAM, 128GB)', '27200', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJmZ_-5HRv8X4FpaVnNNvynUfro9D_uhjN8U1czwwjDz5-Pfx7GT7jh8OxerI&s', '5000mAh with 67W Fast Charging', '6.7-inch AMOLED, 120Hz Refresh Rate', 'MediaTek Dimensity 7050', '50MP + 32MP + 8MP Triple Rear & 32MP Front Camera', 50, 'Electronics'),
(463, 'Oppo F25 Pro 5G (8GB RAM, 128GB)', '21999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlEBFNh3WBNEX-3fOxKod3WoVOcazDLr7mNtgz8LhSXHB1OAtG2PbDZgfLAA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(464, 'Oppo Reno 10 5G (8GB RAM, 256GB)', '26999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlZM0_V2axe_YxF4DcUUbrcJJKpb4sqXQlrTANxKW5Uso5r7_H1YHelJBTnDg&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(466, 'Apple iPhone 15 Pro Max (256GB)', '99499', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQNwAFQHqnB2PPLzqzuZSSbJwb2H94sjH_aQuqlbgCXos4XcJmIVB15nmo7w&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(467, 'Google Pixel 8 Pro (512GB)', '94990', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXlPThar1gr93or4MWaLK4844MJdhG4dIDpH18xmhzQyUuceTG6pU_EUndoxY&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(472, 'Nothing Phone (3a) Pro (8GB RAM, 128GB Storage)', '27999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxUvklmSCj51fKMa0eEFO4nRYkbgG3xkVJCn6oF703jZAM9MMkeNwe2xRUOnw&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(475, 'Iqoo 15R', '44998', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShRTp3iWn3iEaLdnj6JtzIraDGDU--OfRq1h0dwpmiizxqYXJAH7rfVyKimXw&s', '7600mAh', 'AMOLED', 'Qualcomm Snapdragon 8 Gen 5', '50MP Sony LYT-700V (with OIS)', 50, 'Electronics'),
(476, 'Vivo V70 Elite', '51999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQegIe1UPjWNfEP6TgnzlK6msIwIpAGTHntClfez6og7eXO3itOqxfS6aieMg&s', '6500 mAh', 'AMOLED', 'Qualcomm Snapdragon 8s Gen 3', '50MP Wide Angle Primary Camera (with OIS)', 50, 'Electronics'),
(481, 'Realme P4 Power', '29999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwcz2InjqfiOsME3HQTrKM647M1iSqjDDm2R0Djpj0sILhQheHPdup97SvQg&s', '5000mAh', 'AMOLED Display', 'Octa-Core Processor', '50MP Main', 50, 'Electronics'),
(491, 'Motorola Signature', '54366', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4iyUgCi6KyjI-pWYPtNF36ZoQWaT41WlgSRM7dWSt1cuSkD71svbRO9IHYQQ&s', '5200 mAh', 'LTPO AMOLED', 'Qualcomm Snapdragon 8 Gen 5', '50 MP (Sony LYT-828, f/1.6)', 50, 'Electronics'),
(492, 'Oneplus 11R', '30299', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHvo-X0T0D2wVpd3uEXHRvTLTbJdbNV41hnK559iXlP6Cn43IE7F4K2XvlSXg&s', '5000 mAh', 'Super Fluid AMOLED', 'Qualcomm Snapdragon 8+ Gen 1', '50 MP (Sony IMX890) with OIS', 50, 'Electronics'),
(494, 'Oneplus 15R', '47998', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGRpLvnN68PCjcq__upCFPgX_qBKTzgpqgj7g7LQWKu6EtrTIsKuujEhiQzp8&s', '7400mAh', 'LTPS AMOLED', 'Qualcomm Snapdragon 8 Gen 5 (Oryon CPU)', '50MP (Sony IMX906, f/1.8, OIS)', 50, 'Electronics'),
(495, 'Samsung Galaxy S24 Ultra (12GB RAM, 256GB Storage)', '71999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_LOntXvRpUR9M8evfnOgsMZTCl63N5xch_nWIYrP79yRLpN-DTj1KutJC5Zc&s', '5000mAh', '6.8-inch Dynamic AMOLED 2X, QHD+, 120Hz', 'Qualcomm Snapdragon 8 Gen 3', '200MP Main, 50MP Periscope Telephoto, 10MP Telephoto, 12MP Ultrawide', 50, 'Electronics'),
(496, 'Samsung Galaxy S24 Ultra 5G (12GB RAM, 256GB Storage)', '94993', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_LOntXvRpUR9M8evfnOgsMZTCl63N5xch_nWIYrP79yRLpN-DTj1KutJC5Zc&s', '5000mAh', '6.8-inch LTPO AMOLED, 120Hz', 'Qualcomm Snapdragon 8 Gen 3', '200MP Quad Rear Camera', 50, 'Electronics'),
(497, 'Samsung Galaxy Z Fold 5 (12GB RAM, 512GB Storage)', '96999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBFWuFAGbqvtJD1vYYuCp1WuEA-FTZFnURf5xWwBF7MqJZadydBggqwe1h5bg&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(498, 'Samsung Galaxy S23 Ultra 5G (12GB RAM, 256GB Storage)', '76999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwby61R2RqNtMBJtMgzIn_6HG4MYFx-0dCC9ifjCzv0tV-XX73dbIqQTE2jYk&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(500, 'Samsung Galaxy S24 Ultra 5G', '93999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_LOntXvRpUR9M8evfnOgsMZTCl63N5xch_nWIYrP79yRLpN-DTj1KutJC5Zc&s', '5000 mAh', 'Dynamic LTPO AMOLED 2X', 'Qualcomm Snapdragon 8 Gen 3 for Galaxy (SM8650-AC)', '200 MP', 50, 'Electronics'),
(502, 'Xiaomi 14 Ultra (16GB RAM, 512GB Storage)', '99999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1n784qNhE0_jpScU7vscwzVWOc4lqy7AwQguLpJDZ1fAYg9QQwY0WxoRy3jc&s', '5300mAh', '6.73-inch WQHD+ AMOLED, 1-120Hz dynamic refresh rate', 'Snapdragon® 8 Gen 3 Mobile Platform', 'Quad 50MP (main f/1.63, ultra-wide f/1.8, telephoto f/2.5, telephoto f/1.8) + 32MP front', 50, 'Electronics'),
(503, 'Xiaomi 13 Pro 5G (12GB RAM, 256GB Storage)', '54990', 'https://m.media-amazon.com/images/I/61RvCwjI7dL.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(504, 'iQOO 12 5G (12GB RAM, 256GB)', '48875', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSp_ZlP_WQKfsNm_p6V1_-bs4XD3dAQg9q4EGvdQSAr08knQsBt3lhgnB2PDA&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(505, 'Realme P1 5G (6GB RAM, 128GB Storage)', '13999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRf9zQH9myGJJd7niMSwT7EMph0MNb6Bj2sfmqKk3SQs9SvbGb6cEJ5e8MEBA&s', '5000mAh', '6.67-inch 120Hz AMOLED', 'MediaTek Dimensity 7050', '50MP Dual Rear', 50, 'Electronics'),
(506, 'iQOO Z9x 5G (8GB RAM, 128GB Storage)', '14999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaAhA_4j0a1RO2llxB-UkxC__5vbgej24RG6dinM_SHT0VIDmHCSRcSIddOw&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(510, 'Google Pixel 10a', '49999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlWaE401daDkeRWrLxiJdUlWFceuIWErcdKH5-vnLZA18QWvLKFpvfFYCr3Q&s', '5100 mAh', 'pOLED', 'Google Tensor G4', '48 MP, f/1.7', 50, 'Electronics'),
(511, 'OnePlus 12 (16GB RAM, 512GB)', '55799', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQySru_fLtymcqHz35uZnAxXxCvaBsCEAz01j0oAVNXoVmLxe-DuaYNhmj-Ew&s', '5400mAh', '6.82-inch (1440x3168) 120Hz LTPO ProXDR AMOLED', 'Snapdragon 8 Gen 3', '50MP + 64MP + 48MP', 50, 'Electronics'),
(512, 'Vivo X100 Pro (16GB RAM, 512GB)', '58999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbbflqR2S68YX2BK-JzCt3fiaHy7qby4LHaXQEPUnAypDoFSRoeDhriIqR4Q&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(515, 'Apple Iphone 15 Pro Max', '159900', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQNwAFQHqnB2PPLzqzuZSSbJwb2H94sjH_aQuqlbgCXos4XcJmIVB15nmo7w&s', '4441 mAh', 'LTPO Super Retina XDR OLED with ProMotion', 'Apple A17 Pro', '48MP, f/1.78, sensor-shift OIS', 50, 'Electronics'),
(525, 'realme P4 Power 5G', '24485', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4i4OY1qYv4Sp_ZSdvo9TXGG3iooenDQfN-fxR0U0-zBShi2MokVqAhyRYQQ&s', '10,001mAh', 'AMOLED HyperGlow 4D Curve+', 'MediaTek Dimensity 7400 Ultra 5G', '50MP (Sony primary sensor, f/1.8, OIS)', 50, 'Electronics'),
(529, 'Motorola Edge 40 Neo', '20990', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTk5y-tq6w9lotuhL8QRdGSB4H_A0I9UZFmEwTSRz-lXTX3b3X0etMvxzL0yQ&s', 'Standard', 'Standard', '12GB RAM, 256GB Storage, 50MP Dual Rear Camera, 32MP Front Camera, 5000mAh Battery', 'Standard', 50, 'Electronics'),
(530, 'OnePlus Nord CE 2 Lite 5G', '17994', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVmrILA2rZ1-mros-inOYWvO-T9GuyLLF0pEnxIIu7k13UhZkVttnPpjRWTA&s', '5000mAh, 33W SuperVOOC Fast Charging', '6.59 inch IPS LCD, 1080x2412 pixels (FHD+), 120Hz refresh rate', 'Qualcomm Snapdragon 695 5G Octa-core', 'Rear: 64MP (f/1.7) Main + 2MP (f/2.4) Depth + 2MP (f/2.4) Macro; Front: 16MP', 50, 'Mid-range Smartphone'),
(531, 'OnePlus 12 (12GB RAM, 256GB Storage)', '45999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQySru_fLtymcqHz35uZnAxXxCvaBsCEAz01j0oAVNXoVmLxe-DuaYNhmj-Ew&s', '5400mAh', '6.82-inch QHD+ 120Hz LTPO AMOLED', 'Snapdragon 8 Gen 3', '50MP + 48MP + 64MP Triple Rear', 50, 'Electronics'),
(532, 'Samsung Galaxy S24 (8GB RAM, 256GB Storage)', '47999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_LOntXvRpUR9M8evfnOgsMZTCl63N5xch_nWIYrP79yRLpN-DTj1KutJC5Zc&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(538, 'Samsung Galaxy S24 5G', '40999', 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQivRCP7nxp5uOKvgS8kXyurnO4VHoTSU0qRh4MwuopWCTmTs-Oxbu_x5yyuANQRlB7_fGLgTghUN78pOgqzrxK-qdndbvryiyd9X5VCI5VzryaLBryxps58BvyqoDWKjiwcyg60zc&usqp=CAc', '4000 mAh', 'Dynamic AMOLED 2X, LTPO', 'Exynos 2400', '50 MP', 50, 'Electronics'),
(540, 'Samsung Galaxy S23', '44999', 'https://rukminim1.flixcart.com/image/900/900/xif0q/mobile/y/8/i/-original-imah4zp7fgtezhsz.jpeg?q=90\n', '3900 mAh', 'Dynamic AMOLED 2X', 'Qualcomm Snapdragon 8 Gen 2 for Galaxy', '50 MP, f/1.8 (wide)', 50, 'Electronics'),
(541, 'Nothing Phone (2) (8GB RAM, 128GB Storage)', '29999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxUvklmSCj51fKMa0eEFO4nRYkbgG3xkVJCn6oF703jZAM9MMkeNwe2xRUOnw&s', '4700mAh', '6.7-inch 120Hz LTPO AMOLED', 'Qualcomm Snapdragon 8+ Gen 1', '50MP Dual Rear', 50, 'Electronics'),
(542, 'iQOO Neo 10R (8GB RAM, 128GB Storage)', '26998', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9BnAZYbF_JxWakE689d9Ie8Jxjj2UABwhkNp-NJRaQTGYpkdg2waO_KhhCg&s', '6400mAh', '6.78-inch 1.5K AMOLED, 144Hz', 'Snapdragon 8s Gen 3', '50MP', 50, 'Electronics'),
(543, 'Realme P4 Power (8GB RAM, 128GB Storage)', '25999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnERU_phClfJ1fudOBda1jkw42b7AVd4HjGii20SoKZxcSyHSodqafVjQvXds&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(544, 'OnePlus Nord CE5 5G (8GB RAM, 128GB Storage)', '24998', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOXEbBfBAfqzPwBmEIdzn7ZjGpdJOH2bI2c9XMZ0FxRvZ6pCOZmM_hJ8d6UoY&s', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(545, 'Samsung Galaxy S24+ (12GB RAM, 256GB Storage)', '59999', 'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcR4V2oJneSdgrzWIEVaTEtKp69VSj95nf-OuCfnLbieLlEc7kdRU5itwVF88j8wlpesuE0EHwbmdDao1am-oIhl9my9h_7YrF9U_sGHXkkmN8VjzKZmF6FQ9UGpC6QXdW_8rSBwGw&usqp=CAc', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(546, 'Apple Iphone 17 Pro Max', '149900', 'https://www.mobileana.com/wp-content/uploads/2025/06/Apple-iPhone-17-Pro-Max-Cosmic-Orange.webp', '4832 mAh', 'LTPO Super Retina XDR OLED', 'Apple A19 Pro', '48MP Fusion Main, f/1.78, 24mm (wide) with second‑generation sensor‑shift optical image stabilizatio', 50, 'Electronics'),
(550, 'Vivo Y36', '14999', 'https://fdn2.gsmarena.com/vv/bigpic/vivo-x100-pro.jpg', '5000mAh', 'IPS LCD', 'Qualcomm Snapdragon 680', '50 MP, f/1.8 (wide), PDAF', 50, 'Electronics'),
(551, 'Xiaomi Redmi Note 13 Pro 5G (8GB RAM, 128GB Storage)', '25999', 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14-pro.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(552, 'Apple iPhone 15 (128GB)', '54900', 'https://m.media-amazon.com/images/I/71d7rfSl0wL._AC_UF1000,1000_QL80_.jpg', 'Up to 20 hours video playback', '6.1-inch Super Retina XDR OLED, 60Hz', 'Apple A16 Bionic', '48MP Main', 50, 'Electronics'),
(554, 'OnePlus 12R (16GB RAM, 256GB)', '42999', 'https://fdn2.gsmarena.com/vv/bigpic/oneplus-12.jpg', '5500mAh', '6.78-inch LTPO4 AMOLED, 120Hz', 'Qualcomm Snapdragon 8 Gen 2', '50MP', 50, 'Electronics'),
(556, 'Google Pixel 8 (256GB)', '54999', 'https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8-pro.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(588, 'Samsung Galaxy S21', '22999', 'https://cdn.beebom.com/mobile/samsung-galaxy-s21-front-and-back2.png', '4000 mAh', 'Dynamic AMOLED 2X', 'Samsung Exynos 2100 (5 nm) / Qualcomm Snapdragon 888 (5 nm)', '12 MP, f/1.8, 26mm (wide), OIS, PDAF', 50, 'Electronics'),
(592, 'iQOO Neo 9 Pro 5G (12GB RAM, 256GB)', '33999', 'https://rukminim2.flixcart.com/image/832/832/xif0q/cases-covers/back-cover/v/l/w/cndy-pco-c55-4-gdbuy-original-imagye7wtcwfkkhz.jpeg?q=70&crop=false', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(594, 'Samsung Galaxy A25 5G', '18399', 'http://rukmini1.flixcart.com/image/300/300/xif0q/cases-covers/back-cover/6/c/4/21-sam-a25-249-printwhiz-original-imagyyrzjzjjcyqt.jpeg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(597, 'Samsung Galaxy S23 Ultra 5G', '74999', 'https://m.media-amazon.com/images/I/51hqXIAVXAL.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(598, 'OnePlus OnePlus 12', '65000', 'https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/p/g/i/12-cph2573-oneplus-original-imahyzy8wvsewgxx.jpeg?q=70&crop=false', '5400mAh', '6.82 inch Display', 'Snapdragon 8 Gen 3', '50MP Camera', 50, 'Electronics'),
(599, 'Realme Realme GT 7 Pro', '55999', 'https://image01.realme.net/general/20241016/17290429486784c3fd616f5214fb695f6196012ac356e.png?width=1080&height=1080&size=1408866', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(600, 'OPPO OPPO Find X8 Pro', '94999', 'https://www.mobiledokan.com/media/oppo-find-x8-pro-full-back-camera-side-image.webp', '5910mAh', '6.78 inch Display', 'Dimensity 9400', '50MP Camera', 50, 'Electronics'),
(603, 'iQOO iQOO Neo 10R 5G', '28999', 'https://in-exstatic-vivofs.vivo.com/gdHFRinHEMrj3yPG/1741672409928/20eb7eea4aadbc4f9ba3ec7cae271d5b.png', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(605, 'Apple iPhone 16 Plus', '89999', 'https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/j/h/x/-original-imah4jykuzexdzek.jpeg?q=70&crop=false', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(625, 'Samsung Galaxy S24 FE 5G (8GB RAM, 256GB)', '45999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//preview.redd.it/galaxy-s24-fe-official-renders-v0-rh92bl23xthd1.jpg%3Fwidth%3D640%26crop%3Dsmart%26auto%3Dwebp%26s%3Dcaf599f207f0d1a4027e227a79ba0037d3ec58c2', '4700mAh', '6.7 inch Display', 'Exynos 2500', '50MP Camera', 50, 'Electronics'),
(626, 'Samsung Galaxy S24 FE 5G (8GB RAM, 512GB)', '49678', 'https://external-content.duckduckgo.com/iu/?u=https%3A//preview.redd.it/galaxy-s24-fe-official-renders-v0-rh92bl23xthd1.jpg%3Fwidth%3D640%26crop%3Dsmart%26auto%3Dwebp%26s%3Dcaf599f207f0d1a4027e227a79ba0037d3ec58c2', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(627, 'Samsung Galaxy S24 FE 5G (16GB RAM, 256GB)', '51518', 'https://external-content.duckduckgo.com/iu/?u=https%3A//m.media-amazon.com/images/I/61bXUCHBw%2BL.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(628, 'OPPO Find X8 Pro 5G (16GB RAM, 512GB)', '94999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.oppo.com/content/dam/oppo/product-asset-library/find/find-x8-series/en/oppo-find-x8-pro/white-apac/assets/images-color-konka-b-1-mo.png', '5910mAh', '6.78 inch Display', 'Dimensity 9400', '50MP Camera', 50, 'Electronics'),
(629, 'OPPO Find X8 Pro 5G (16GB RAM, 1024GB)', '102598', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.oppo.com/content/dam/oppo/product-asset-library/find/find-x8-series/en/oppo-find-x8-pro/white-apac/assets/images-color-konka-b-1-mo.png', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(630, 'OPPO Find X8 Pro 5G (32GB RAM, 512GB)', '106398', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.oppo.com/content/dam/oppo/product-asset-library/find/find-x8-series/en/oppo-find-x8-pro/white-apac/assets/images-color-konka-b-1-mo.png', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(631, 'OnePlus 13 5G (12GB RAM, 256GB)', '69999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//oasis.opstatics.com/content/dam/oasis/page/2024/global/phones/13/specs/13-white.png', '6000mAh', '6.82 inch Display', 'Snapdragon 8 Elite', '50MP Camera', 50, 'Electronics'),
(632, 'OnePlus 13 5G (12GB RAM, 512GB)', '75598', 'https://external-content.duckduckgo.com/iu/?u=https%3A//oasis.opstatics.com/content/dam/oasis/page/2024/global/phones/13/specs/13-white.png', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(633, 'Samsung Galaxy S24 FE (8GB RAM, 128GB) 5G', '39995', 'https://external-content.duckduckgo.com/iu/?u=https%3A//m.media-amazon.com/images/I/61bXUCHBw%2BL.jpg', '4700mAh', '6.7-inch 120Hz Dynamic AMOLED 2X', 'Exynos 2400e', '50MP + 12MP + 8MP Triple Rear Camera', 50, 'Electronics'),
(634, 'Samsung Galaxy A55 5G (8GB RAM, 128GB)', '31499', 'https://external-content.duckduckgo.com/iu/?u=https%3A//static0.anpoimages.com/wordpress/wp-content/uploads/2024/03/galaxy-a55-a35-2.jpg%3Fq%3D50%26fit%3Dcrop%26w%3D825%26dpr%3D1.5', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(635, 'Samsung Galaxy S23 FE (8GB RAM, 128GB)', '39995', 'https://external-content.duckduckgo.com/iu/?u=https%3A//cdn.mos.cms.futurecdn.net/MXbbBGmkgPNAKqoZSgeEdS.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(636, 'Apple iPhone 17 5G (8GB RAM, 256GB)', '89999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.apple.com/newsroom/images/2025/09/apple-debuts-iphone-17/tile/Apple-iPhone-17-hero-250909-lp.jpg.news_app_ed.jpg', '4000mAh', '6.1 inch Display', 'A19', '48MP Camera', 50, 'Electronics'),
(637, 'Apple iPhone 16 Plus 5G (8GB RAM, 128GB)', '89999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.apple.com/newsroom/images/2024/09/apple-introduces-iphone-16-and-iphone-16-plus/tile/Apple-iPhone-16-lineup-240909-lp.jpg.landing-big_2x.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(638, 'Apple iPhone 16 5G (8GB RAM, 128GB)', '79999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//img.freepik.com/premium-vector/apple-iphone-16-white-isolated-white-background_570051-851.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(645, 'Samsung Galaxy S26 Ultra', '139999', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkDf4r08NojgKkTgPdKFFn0sgFzTqJfQ60-qSq-CHjDnvGfsL-R1xFsFCA6A&s', '5000mAh', 'Dynamic LTPO AMOLED 2X', 'Qualcomm Snapdragon 8 Elite Gen 5 for Galaxy (3nm)', '200 MP Wide Angle Primary Camera (F1.4, OIS)', 50, 'Electronics'),
(646, 'Samsung S23', '49999', 'https://www.google.com/imgres?q=samsung%20s23&imgurl=https%3A%2F%2Frukminim2.flixcart.com%2Fimage%2F480%2F640%2Fxif0q%2Fmobile%2Fy%2F8%2Fi%2F-original-imah4zp7fgtezhsz.jpeg%3Fq%3D90&imgrefurl=https%3A%2F%2Fwww.flipkart.com%2Fsamsung-galaxy-s23-5g-cream-256-gb%2Fp%2Fitm745d4b532623e&docid=fW2PDYrtEnxr8M&tbnid=gu5LvohCgH_AbM&vet=12ahUKEwjk1Nnkh6uTAxXYXGwGHY1iJVEQnPAOegQIFBAB..i&w=480&h=480&hcb=2&ved=2ahUKEwjk1Nnkh6uTAxXYXGwGHY1iJVEQnPAOegQIFBAB', '3900mAh', 'Dynamic LTPO AMOLED 2X', 'Qualcomm SM8550-AC Snapdragon 8 Gen 2 (4 nm)', '50 MP, f/1.8, 24mm (wide), 1/1.56\", 1.0µm, dual pixel PDAF, OIS', 50, 'Electronics'),
(655, 'Samsung Galaxy A56 5G (8GB RAM, 256GB)', '24999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//m-cdn.phonearena.com/images/article/166481-wide-two_1200/Samsung-Galaxy-A56-5G-passes-MIIT-certification-Dual-SIM-Android-15-and-a-5000mah-battery.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(656, 'Samsung Galaxy F55 5G (8GB RAM, 256GB)', '25000', 'https://external-content.duckduckgo.com/iu/?u=https%3A//i.gadgets360cdn.com/large/samsung_galaxy_f55_5g_google_play_console_91mobiles_inline_1713762062507.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(657, 'Apple iPhone 16e 5G (8GB RAM, 128GB)', '59999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.apple.com/newsroom/images/2025/02/apple-debuts-iphone-16e-a-powerful-new-member-of-the-iphone-16-family/article/Apple-iPhone-16e-hero-250219_inline.jpg.large.jpg', '3279mAh', '6.1 inch Display', 'A16', '48MP Camera', 50, 'Electronics'),
(658, 'Apple iPhone 13 (4GB RAM, 128GB)', '49000', 'https://external-content.duckduckgo.com/iu/?u=https%3A//m.media-amazon.com/images/I/7199VOAdkRL.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(659, 'Samsung S23 - Tactical Edition', '0', 'https://external-content.duckduckgo.com/iu/?u=https%3A//img.us.news.samsung.com/us/wp-content/uploads/2023/09/19212411/s23-tactical-600x453.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(660, 'Samsung S24', '0', 'https://external-content.duckduckgo.com/iu/?u=https%3A//static0.pocketlintimages.com/wordpress/wp-content/uploads/2023/09/samsung-galaxy-s24-front-and-back.jpg%3Fq%3D50%26fit%3Dcrop%26w%3D750%26dpr%3D1.5', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(661, 'Samsung S22', '0', 'https://external-content.duckduckgo.com/iu/?u=https%3A//img.global.news.samsung.com/global/wp-content/uploads/2022/02/Galaxy-S22-S22-pr_main3.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(662, 'Samsung Galaxy S24 5G Ai', '0', 'https://external-content.duckduckgo.com/iu/?u=https%3A//static0.pocketlintimages.com/wordpress/wp-content/uploads/2023/09/samsung-galaxy-s24-front-and-back.jpg%3Fq%3D50%26fit%3Dcrop%26w%3D750%26dpr%3D1.5', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(663, 'Samsung Galaxy S24 Fe 5G Ai', '0', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.dxomark.com/wp-content/uploads/medias/post-178742/Samsung-Galaxy-S24-FE_featured-image-packshot-review-1.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(664, 'Motorola Edge 30 5G', '24999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//motorolaroe.vtexassets.com/arquivos/ids/156815/Motorola-edge-30-pdp-render-Mojito-4-31f5yjhf.png%3Fv%3D637864930876170000', '4020mAh, 33W TurboPower Fast Charging', '6.5-inch AMOLED, FHD+ (2400 x 1080), 144Hz refresh rate, HDR10+', 'Qualcomm Snapdragon 778G+ 5G', 'Rear: 50MP Main (OIS) + 50MP Ultra-wide (114° FOV, Macro Vision) + 2MP Depth; Front: 32MP', 50, 'Mid-Range Smartphone'),
(665, 'TECNO POVA 5 Pro 5G', '14999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//i.ebayimg.com/images/g/S6QAAOSw6E5m2C0i/s-l400.jpg', '5000 mAh, 68W Ultra Fast Charging', '6.78-inch IPS LCD, Full HD+ (2460 x 1080 pixels), 120Hz Refresh Rate, 580 nits peak brightness', 'MediaTek Dimensity 6080 Octa-core SoC (up to 2.4 GHz)', '50MP Main Camera (f/1.6, PDAF) + 0.08MP AI Lens (Depth Sensor) (Dual Rear), 16MP Front Camera', 50, 'Mid-Range Smartphone'),
(666, 'Vivo V30 Pro', '41999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//asia-exstatic-vivofs.vivo.com/PSee2l50xoirPK7y/product/1713262501446/zip/img/mobi/kv-bg.jpg', '5000mAh, 80W FlashCharge', '6.78-inch AMOLED, 120Hz Refresh Rate, 2800 x 1260 pixels (1.5K resolution), 2800 nits Local Peak Bri', 'MediaTek Dimensity 8200-Ultra', 'Rear: 50MP VCS True Color Main Camera (Sony IMX920, OIS), 50MP AF Ultra Wide-Angle Camera, 50MP ZEIS', 50, 'Mid-Range Smartphone'),
(667, 'OnePlus Nord CE 3 Lite 5G', '18999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//owp.klarna.com/product/640x640/3010066883/OnePlus-Nord-CE-3-Lite-5G-256GB.jpg%3Fph%3Dtrue', '5000mAh, 67W SUPERVOOC Fast Charging', '6.72-inch IPS LCD, 120Hz refresh rate, 1080 x 2400 pixels (FHD+)', 'Qualcomm Snapdragon 695 5G', 'Rear: 108MP Main with EIS, 2MP Depth, 2MP Macro; Front: 16MP', 50, 'Mid-Range Smartphone'),
(668, 'iQOO Z9 Lite 5G (4GB RAM, 128GB)', '11000', 'https://external-content.duckduckgo.com/iu/?u=https%3A//in-exstatic-vivofs.vivo.com/gdHFRinHEMrj3yPG/1721021583359/30a2ba7477ef4018482685daba5932d9.png', '5000mAh', '6.56 inch Display', 'Snapdragon 4 Gen 2', '50MP Camera', 50, 'Electronics');
INSERT INTO `product` (`id`, `name`, `price`, `image_url`, `battery_spec`, `display_spec`, `processor_spec`, `camera_spec`, `stock`, `category`) VALUES
(669, 'Poco C75 5G (6GB RAM, 128GB)', '10999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//m.media-amazon.com/images/I/51g67nroW9L._AC_UF350%2C350_QL80_.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(670, 'Xiaomi Redmi 13R 5G (4GB RAM, 128GB)', '9999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.notebookcheck.net/fileadmin/_processed_/webp/Notebooks/News/_nc3/Xiaomi13edit-q82-w2560-h.webp', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(682, 'Samsung Galaxy S25 Plus 5G (12GB RAM, 256GB)', '99000', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.androidheadlines.com/wp-content/uploads/2025/01/Samsung-Galaxy-S25-official-render-1-1420x1420.webp', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(683, 'Xiaomi 15 5G (12GB RAM, 256GB)', '81999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//cdn.wccftech.com/wp-content/uploads/2024/10/Xiaomi-15-10-1456x1265.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(684, 'Samsung Galaxy S25 5G (12GB RAM, 256GB)', '80000', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.androidheadlines.com/wp-content/uploads/2025/01/Samsung-Galaxy-S25-official-render-1-1420x1420.webp', '4000mAh', '6.2 inch Display', 'Snapdragon 8 Elite', '50MP Camera', 50, 'Electronics'),
(685, 'OnePlus 13s 5G (16GB RAM, 512GB)', '79999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//oasis.opstatics.com/content/dam/oasis/page/2024/global/phones/13/specs/13-white.png', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(692, 'Tecno Pova 3', '6999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//d13pvy8xd75yde.cloudfront.net/global/phones/POVA3/pova3--yin.png', '7000mAh', 'IPS LCD', 'MediaTek Helio G88', '50MP', 50, 'Electronics'),
(693, 'Tecno Pova', '10449', 'https://external-content.duckduckgo.com/iu/?u=https%3A//d13pvy8xd75yde.cloudfront.net/phones/lj8k/pova7%25E7%25B3%25BB%25E7%25B1%25BB800%25E5%259B%25BE/LJ9.png', '6000 mAh', 'IPS LCD', 'MediaTek Helio G80', '16 MP (f/1.85)', 50, 'Electronics'),
(694, 'Poco C61 (4GB RAM, 64GB)', '7499', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.elryan.com/img/600/600/resize/catalog/product/p/o/poco_c61-ds-4-128-white.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(695, 'Xiaomi 15 Ultra 5G (16GB RAM, 512GB)', '109999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//bludiode.com/57319/xiaomi-15-ultra-16gb1tb-white.jpg', '5000mAh', '6.73 inch Display', 'Snapdragon 8 Elite', '50MP Camera', 50, 'Electronics'),
(696, 'Xiaomi 14 Ultra 5G (16GB RAM, 512GB)', '99000', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.qualcomm.com/content/dam/qcomm-martech/dm-assets/images/device/image/xiaomi-14-ultra.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(697, 'Google Pixel 9 Pro 5G (16GB RAM, 256GB)', '99999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//www.dxomark.com/wp-content/uploads/medias/post-176190/Google-Pixel-9-Pro-XL_Yoast-image-packshot-review.png', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(698, 'Asus ROG Phone 8 Pro 5G (16GB RAM, 512GB)', '109999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//external-preview.redd.it/exclusive-asus-rog-phone-8-pro-official-high-res-renders-v0-7Gs6usosFkE0vDQONu4rq5zimjBZMrKI53jGYFudpng.jpg%3Fauto%3Dwebp%26s%3D3cb7db1b4ba312b1b42c5204f2ce5b6b053aa84f', '5500mAh', '6.78 inch Display', 'Snapdragon 8 Gen 3', '50MP Camera', 50, 'Electronics'),
(699, 'Asus ROG Phone 9 5G (16GB RAM, 256GB)', '99999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//dlcdnwebimgs.asus.com/gain/428A70F4-5A08-416A-8BDA-069DD27E28F4', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(700, 'iQOO 13 5G (16GB RAM, 512GB)', '70198', 'https://external-content.duckduckgo.com/iu/?u=https%3A//asia-exstatic-vivofs.vivo.com/PSee2l50xoirPK7y/1732527226902/13fc0816985cca09a079801127889d67.png', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(701, 'Sony Xperia 10 VI 5G (6GB RAM, 256GB)', '43198', 'https://external-content.duckduckgo.com/iu/?u=https%3A//gagadget.com/media/uploads/sony-xperia-10-vi-rendes-2.jpg', '5000mAh', '6.1 inch Display', 'Snapdragon 6 Gen 1', '48MP Camera', 50, 'Electronics'),
(702, 'Asus ROG Phone 9 Pro 5G (24GB RAM, 1024GB)', '129999', 'https://external-content.duckduckgo.com/iu/?u=https%3A//dlcdnwebimgs.asus.com/gain/BC2CEA28-F482-473E-9071-C82787E76A5B/w260/fwebp', '5800mAh', '6.78 inch Display', 'Snapdragon 8 Elite', '50MP Camera', 50, 'Electronics'),
(703, 'Asus ROG Phone 9 5G (32GB RAM, 256GB)', '111998', 'https://external-content.duckduckgo.com/iu/?u=https%3A//press.asus.com/assets/w_2400%2Ch_2400/f3e5dec6-35ea-4d60-b064-8de84597c62c/ROG%2520Phone%25209_Group%2520Photo_04.jpg', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(704, 'Asus ROG Phone 8 Pro 5G (16GB RAM, 1024GB)', '118798', 'https://external-content.duckduckgo.com/iu/?u=https%3A//press.asus.com/assets/w_640%2Ch_640/d47892a0-e09c-4a1e-b23c-dbe20c919559/ROG%2520Phone%25208%2520Pro-03%2520%281%29.png', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(705, 'Samsung Galaxy F06 5G (6GB RAM, 256GB)', '10798', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.samsung.com%2Fis%2Fimage%2Fsamsung%2Fp6pim%2Fin%2Fsm-e066bzvhins%2Fgallery%2Fin-galaxy-f-sm-e066bzvhins-sm-e---bzvgins-thumb-545132359&f=1&nofb=1', '5000mAh', '6.74 inch Display', 'Dimensity 6300', '50MP Camera', 50, 'Electronics'),
(706, 'Nothing CMF Phone 1 5G (6GB RAM, 128GB)', '15999', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F51Zv4RzFhRL._AC_UF350%2C350_QL50_.jpg&f=1&nofb=1', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(707, 'OPPO A60 5G (8GB RAM, 128GB)', '16000', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.oppo.com%2Fcontent%2Fdam%2Foppo%2Fcommon%2Fmkt%2Fv2-2%2Foppo-a60%2Flist-page%2F427-600-blue.png&f=1&nofb=1', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(708, 'Samsung S26', '87999', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F71JN2VbCqqL._AC_UF894%2C1000_QL80_.jpg&f=1&nofb=1', '5000mAh', 'AMOLED Display', 'Octa-Core Processor', '50MP Main Camera', 50, 'Electronics'),
(709, 'Samsung S27', '0', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.tatacroma.com%2FCroma%2520Assets%2FCommunication%2FMobiles%2FImages%2F321487_0_ivSr5GKkj.png%3FupdatedAt%3D1772089657873&f=1&nofb=1', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(710, 'Samsung S25', '0', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F41-Bc14cmeL.jpg&f=1&nofb=1', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(712, 'Nothing Phone 4A', '33652', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.shopify.com%2Fs%2Ffiles%2F1%2F0586%2F3270%2F0077%2Ffiles%2FPhone-4a-Pro-White.png%3Fv%3D1772251228&f=1&nofb=1', '5000mAh', 'AMOLED Display', 'Octa-Core Processor', '50MP Main Camera', 50, 'Electronics'),
(722, 'Motorola Edge 70 Fusion', '24999', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmotorolain.vtexassets.com%2Farquivos%2Fids%2F161666%2Fmotorola-edge-70-fusion-pdp-ecom-render-06-color5-4zlgawe8.png%3Fv%3D639072888087570000&f=1&nofb=1', '7000mAh (Silicon-Carbon)', '6.78-inch 1.5K Extreme AMOLED Quad Curved Display', 'Qualcomm Snapdragon 7s Gen 4', '50MP Sony LYTIA 710 sensor, OIS, f/1.8 aperture', 50, 'Electronics'),
(727, 'Google Pixel 9a 5G (8GB RAM, 256GB)', '44999', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Flh3.googleusercontent.com%2FU7uX1PJPUuzPWGy_Q4QjJEALaZ6xHfS04XupIYDOSN8h4WAI3uQaEYUtngm9mECiejsX_4NwpT3krOiccCAbo13qNR0R3T3RXXTk%3Ds2046-w2046-e365-rw-v0-nu&f=1&nofb=1', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(728, 'OnePlus Nord 4 5G (8GB RAM, 256GB)', '30000', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimage01-in.oneplus.net%2Fmedia%2F202407%2F08%2F8bb6170dd07822e3bf9ae62a30e00a5a.png&f=1&nofb=1', '5500mAh', '6.74 inch Display', 'Snapdragon 7+ Gen 3', '50MP Camera', 50, 'Electronics'),
(729, 'Nothing Phone 4a 5G (8GB RAM, 512GB)', '31318', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.shopify.com%2Fs%2Ffiles%2F1%2F0586%2F3270%2F0077%2Ffiles%2FPhone-4a-Pro-White.png%3Fv%3D1772251228&f=1&nofb=1', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(730, 'Nothing Phone 2a Plus 5G (12GB RAM, 512GB)', '30240', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.shopify.com%2Fs%2Ffiles%2F1%2F0585%2F2479%2F5086%2Ffiles%2FPhone2aplus-gray-1_1352x1352_0dcf04d6-49e6-46ad-bd43-e20599cdcd2c.png%3Fv%3D1725349781&f=1&nofb=1', 'Standard', 'Standard', 'Standard', 'Standard', 50, 'Electronics'),
(737, 'Xiaomi Poco F6 5G (12GB RAM, 256GB)', '30000', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.beebom.com%2Fmobile%2Fpoco-f6-titanium-front-and-back.png&f=1&nofb=1', '4500mAh', '6.67 inch Display', 'Snapdragon 8s Gen 3', '50MP Camera', 50, 'Electronics'),
(739, 'iQOO Neo 10 5G (8GB RAM, 256GB)', '34999', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fin-exstatic-vivofs.vivo.com%2FgdHFRinHEMrj3yPG%2F1749530161954%2Fd71af840e59cbb6d59bc929c1323e141.png&f=1&nofb=1', '6000mAh', '6.78 inch Display', 'Snapdragon 8s Gen 4', '50MP Camera', 50, 'Electronics'),
(740, 'OPPO A80 5G (16GB RAM, 512GB)', '24778', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pbtech.com%2Fpacific%2Fimgprod%2FM%2FP%2FMPHOPP026391__4.jpg&f=1&nofb=1', '5000mAh', '6.67 inch Display', 'Dimensity 7050', '50MP Camera', 50, 'Electronics'),
(741, 'Samsung Galaxy M55 5G (8GB RAM, 256GB)', '27000', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F81317ePW5sL.jpg&f=1&nofb=1', '6000mAh', '6.7 inch Display', 'Snapdragon 7 Gen 1', '50MP Camera', 50, 'Electronics'),
(742, 'Samsung Galaxy M56 5G (8GB RAM, 256GB)', '29999', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F71hN1gfzDcL.jpg&f=1&nofb=1', '5000mAh', '6.73 inch Display', 'Exynos 1480', '50MP Camera', 50, 'Electronics');

-- --------------------------------------------------------

--
-- Table structure for table `saved_payment_method`
--

CREATE TABLE `saved_payment_method` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `method_type` varchar(50) NOT NULL,
  `details` varchar(255) NOT NULL,
  `expiry` varchar(10) DEFAULT NULL,
  `is_primary` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `password` varchar(60) NOT NULL,
  `reg_date` datetime DEFAULT NULL,
  `is_blocked` tinyint(1) DEFAULT 0,
  `fcm_token` varchar(255) DEFAULT NULL,
  `reset_otp` varchar(10) DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL,
  `fcm_token_android` varchar(255) DEFAULT NULL,
  `fcm_token_web` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `full_name`, `email`, `mobile`, `password`, `reg_date`, `is_blocked`, `fcm_token`, `reset_otp`, `otp_expiry`, `fcm_token_android`, `fcm_token_web`) VALUES
(1, 'Nithyanandhan', 'nithyanandhan205@gmail.com', '9363441126', '$2b$12$kaxrF6OzoM/Et3maQD/1o.GgjcMtZVb9wjR..jT55sExrZCE.uTrm', NULL, 0, 'e5EV62CjTlWkr-9zVwZjRX:APA91bEQVQivRVK-hSFkJ3iiZ84UZMaETqSwM6hQ9FSsVv88CTgte4fY13B-r9yAFFtGou0FeJjlrAqmpsva94m4AaTsfxGeAU89fxQY09Ujhyr1z7_G8XI', '411090', '2026-03-04 10:33:44', 'eOFoQ2hZTdOFqIce98iLKq:APA91bGTKmc0Ie8iFzeKK-qeVyDyJzGXHX0eox47vlvdo-lP3Sgfv_y9MCe7V4Sq_VT3ZOZe6a4c-DjSNcrt3pQfMOVR_mU6zLwCQtEf1joeRd_BrN8R7to', 'e1j3JIPLEQTaTREyMtJD-D:APA91bE-XC6SDy9UFRaKxYitD4_I1I7k78tjQqhirSPCFrbRgnoasdFxtsL26DixGbwTA_GeWzxt1O0gmJMeS4lL_DzYEWqG4VHLiZXBiiSOsIPTF9YbXz4'),
(2, 'Ranjithkumar ', 'ranjithkumarr0687.sse@saveetha.com', '9843945196', '$2b$12$z8tFZYhhMyETPmlUtSidl.dJtHgAhoUmJXYU3BTbxsV.umqq8CVqe', NULL, 0, NULL, NULL, NULL, NULL, NULL),
(3, 'Karthik ', 'karthi@gmail.com', '6353451967', '$2b$12$4tOyj1gn0OG9Y4UEDcZ6DO59mY4.MFxCaiALpg3CnbTcHLgxhBIqy', NULL, 0, NULL, NULL, NULL, NULL, NULL),
(5, 'Enterprise Admin', 'admin@gmail.com', '9999999999', '$2b$12$DrNDnMKvLx403Hm6JS0PY.HjqKlfOzzUPMwVBCyZohAMpC.JbJuhy', NULL, 0, NULL, NULL, NULL, NULL, 'e1j3JIPLEQTaTREyMtJD-D:APA91bE-XC6SDy9UFRaKxYitD4_I1I7k78tjQqhirSPCFrbRgnoasdFxtsL26DixGbwTA_GeWzxt1O0gmJMeS4lL_DzYEWqG4VHLiZXBiiSOsIPTF9YbXz4'),
(9, 'Nithyanandhan R', 'rn620086@gmail.com', '9080874482', '$2b$12$ZIbFSDzWNEMsjHjobe94vu8syuZrrPNE.aj.JyZ41r0aJRIt/Wwe2', '2026-03-08 07:56:21', 0, NULL, NULL, NULL, 'eOFoQ2hZTdOFqIce98iLKq:APA91bGTKmc0Ie8iFzeKK-qeVyDyJzGXHX0eox47vlvdo-lP3Sgfv_y9MCe7V4Sq_VT3ZOZe6a4c-DjSNcrt3pQfMOVR_mU6zLwCQtEf1joeRd_BrN8R7to', NULL),
(13, 'Lakshmi R', 'rameshlakshmi374@gmail.com', '7603966531', '$2b$12$5njUlnUYYnfsgieE5miW/eYIcT3E9L6pu//TY9q2UxfyLO2bq.IGK', '2026-03-08 08:51:06', 0, NULL, NULL, NULL, NULL, NULL),
(15, 'r', 'worksaveetha@gmail.com', '1258963470', '$2b$12$SRqO/M1m3NdyplYyZYKqFOBWpd4kwrZr/Y5cqctCd3KadaSr/dCsO', '2026-03-23 03:29:15', 0, NULL, NULL, NULL, 'eOFoQ2hZTdOFqIce98iLKq:APA91bGTKmc0Ie8iFzeKK-qeVyDyJzGXHX0eox47vlvdo-lP3Sgfv_y9MCe7V4Sq_VT3ZOZe6a4c-DjSNcrt3pQfMOVR_mU6zLwCQtEf1joeRd_BrN8R7to', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `warranty`
--

CREATE TABLE `warranty` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `device_name` varchar(100) NOT NULL,
  `device_type` varchar(50) DEFAULT NULL,
  `expiry_date` datetime NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `invoice_url` varchar(255) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `claim_issue_type` varchar(100) DEFAULT NULL,
  `claim_description` text DEFAULT NULL,
  `claim_invoice_url` varchar(255) DEFAULT NULL,
  `claim_device_url` varchar(255) DEFAULT NULL,
  `service_mode` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `warranty`
--

INSERT INTO `warranty` (`id`, `user_id`, `device_name`, `device_type`, `expiry_date`, `status`, `product_id`, `invoice_url`, `purchase_date`, `claim_issue_type`, `claim_description`, `claim_invoice_url`, `claim_device_url`, `service_mode`) VALUES
(76, 1, 'Nothing Phone 2a Plus 5G (12GB RAM, 512GB)', 'Smartphone', '2029-03-13 00:00:00', 'Secure', 730, NULL, '2026-03-24', 'repair (center)', 'lksjklf', '/static/uploads/claim_76_invoice_Mobiqo_Invoice_INV-3OR4TPLM.pdf', '/static/uploads/claim_76_device_Internship_Exam_24-03-2026_to_28-03-2026_over_all_List.pdf', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `ai_search_log`
--
ALTER TABLE `ai_search_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ai_setting`
--
ALTER TABLE `ai_setting`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `compare_device_cache`
--
ALTER TABLE `compare_device_cache`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `search_query` (`search_query`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `notification_preference`
--
ALTER TABLE `notification_preference`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `invoice_no` (`invoice_no`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `transaction_id` (`transaction_id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indexes for table `privacy_setting`
--
ALTER TABLE `privacy_setting`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `saved_payment_method`
--
ALTER TABLE `saved_payment_method`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `warranty`
--
ALTER TABLE `warranty`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `address`
--
ALTER TABLE `address`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `ai_search_log`
--
ALTER TABLE `ai_search_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;

--
-- AUTO_INCREMENT for table `ai_setting`
--
ALTER TABLE `ai_setting`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `compare_device_cache`
--
ALTER TABLE `compare_device_cache`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notification_preference`
--
ALTER TABLE `notification_preference`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=80;

--
-- AUTO_INCREMENT for table `privacy_setting`
--
ALTER TABLE `privacy_setting`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=743;

--
-- AUTO_INCREMENT for table `saved_payment_method`
--
ALTER TABLE `saved_payment_method`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `warranty`
--
ALTER TABLE `warranty`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `address`
--
ALTER TABLE `address`
  ADD CONSTRAINT `address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `notification_preference`
--
ALTER TABLE `notification_preference`
  ADD CONSTRAINT `notification_preference_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `order_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`);

--
-- Constraints for table `privacy_setting`
--
ALTER TABLE `privacy_setting`
  ADD CONSTRAINT `privacy_setting_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `saved_payment_method`
--
ALTER TABLE `saved_payment_method`
  ADD CONSTRAINT `saved_payment_method_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `warranty`
--
ALTER TABLE `warranty`
  ADD CONSTRAINT `warranty_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

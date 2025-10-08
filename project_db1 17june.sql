-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 18, 2025 at 06:25 AM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project_db1`
--

-- --------------------------------------------------------

--
-- Table structure for table `completed_projects`
--

CREATE TABLE `completed_projects` (
  `id` int(11) NOT NULL,
  `project_title` varchar(255) NOT NULL,
  `domain` varchar(100) NOT NULL,
  `abstract` text NOT NULL,
  `lead_researcher` varchar(100) NOT NULL,
  `supervisor` varchar(100) NOT NULL,
  `completion_date` date NOT NULL,
  `poster_path` varchar(255) DEFAULT NULL,
  `video_path` varchar(255) DEFAULT NULL,
  `report_path` varchar(255) DEFAULT NULL,
  `faculty` varchar(100) DEFAULT NULL,
  `programme` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `completed_projects`
--

INSERT INTO `completed_projects` (`id`, `project_title`, `domain`, `abstract`, `lead_researcher`, `supervisor`, `completion_date`, `poster_path`, `video_path`, `report_path`, `faculty`, `programme`, `created_at`) VALUES
(2, 'Completed Project 001', 'Robotics & Automation', 'Test Completed Project 1 Test Completed Project 1 Test Completed Project 1 Test Completed Project 1 Test Completed Project 1 Test Completed Project 1 Test Completed Project 1 ', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', '2025-05-17', 'uploads/poster_1745821973.67478_Project_Title_-_001_Poster.png', 'uploads/video_1745821973.676775_Project_Title_-_001_Demo_Video.mp4', 'uploads/report_1745821973.676775_IRADA_Intra-University_Innovation_Challenge_Brochure_Final.pdf', 'Faculty of Mathematics and Dat Science', 'BS Software Engineering', '2025-04-28 06:32:53'),
(4, 'AI-driven Image Generation', 'AI & Machine Learning', 'This AI tool uses machine learning to generate realistic and creative images based on user prompts, transforming text descriptions into visually compelling artwork or conceptual illustrations.', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', '2025-04-04', 'uploads/poster_1745904957.467991_nao.png', 'uploads/video_1745904957.468989_AI-driven-video1.mp4', 'uploads/report_1745904957.468989_IRADA_Intra-University_Innovation_Challenge_Brochure_Final.pdf', 'Faculty of Mathematics and Dat Science', 'Bachelors of Science in Software Engineering', '2025-04-29 05:35:57'),
(5, 'Completed Project 002', 'Robotics & Automation', 'Completed Project 002 Completed Project 002 Completed Project 002 Completed Project 002 Completed Project 002 Completed Project 002 Completed Project 002 Completed Project 002', 'Aylin Fatima', 'Dr. Hannah Al Ali', '2025-01-02', 'uploads/poster_1745905433.726972_Completed_Project_1_Poster.png', 'uploads/video_1745905433.727969_AI-driven-video1.mp4', 'uploads/report_1745905433.728966_EAU_AIxplore_2025_Flyer_Layout.docx', 'Faculty of Mathematics and Dat Science', 'Bs Data Science', '2025-04-29 05:42:20'),
(6, 'Completed Project 003', 'Aviation Innovation', 'Completed Project 003 Completed Project 003 Completed Project 003 Completed Project 003 Completed Project 003 Completed Project 003 Completed Project 003 Completed Project 003', 'Ayan Ahmed', 'Dr. Hannah Al Ali', '2024-12-27', 'uploads/poster_1745905534.064162_1.png', 'uploads/video_1745905534.064162_AI-driven-video1.mp4', 'uploads/report_1745905534.065159_proposal_form_2.pdf', 'Faculty of Mathematics and Dat Science', 'Bs Data Science', '2025-04-29 05:45:34'),
(8, 'Completed Project 004', 'Aviation Innovation', 'Completed Project 004 Completed Project 004 Completed Project 004 Completed Project 004 Completed Project 004 Completed Project 004 Completed Project 004 Completed Project 004\r\n', 'Hamad Aslam', 'Dr. Hannah Al Ali', '2025-05-21', 'static\\poster_1747997241.361745_pepper3_1.png', 'static\\video_1747997241.362743_video_1745821973.676775_Project_Title_-_001_Demo_Video_1.mp4', 'static\\report_1747997241.362743_IRADA_Project_Proposal_Template_2.docx', 'Faculty of Mathematics and Data Science', 'Bs AI', '2025-05-23 10:47:21');

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `excerpt` text NOT NULL,
  `event_date` varchar(100) NOT NULL,
  `event_type` varchar(100) NOT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `details` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`id`, `title`, `excerpt`, `event_date`, `event_type`, `image_path`, `details`, `created_at`, `updated_at`) VALUES
(11, 'AI Xplore Cometition', 'Intra-university innovation challenge in AI, Data Science & Robotics for undergraduate students.', 'May 30 - Nov 4, 2025', 'Competition', 'static/uploads/event_1747388976.526271_event1.png', '            <div class=\"modal-body\">\r\n                <h3>About the Challenge</h3>\r\n                <p>The Centre for Innovation in Robotics, Artificial Intelligence, Data Science, and Aviation (IRADA) at Emirates Aviation University is excited to announce <strong>EAU AIxplore 2025: IRADA Intra-University Innovation Challenge in AI, Data Science & Robotics</strong>—a prestigious platform for undergraduate students from various disciplines to demonstrate their creativity, problem-solving skills, and technical expertise.</p>\r\n                \r\n                <h3>Competition Structure</h3>\r\n                <p>The competition is structured in two phases:</p>\r\n                <ul>\r\n                    <li><strong>Phase 1: Project Proposal Submission (April 30, 2025)</strong> - Submit proposals addressing key challenges in Data Science, AI, and Robotics across various sectors.</li>\r\n                    <li><strong>Phase 2: Final Project Submission & Presentation (October 2, 2025)</strong> - Develop and present projects before expert judges.</li>\r\n                </ul>\r\n                \r\n                <h3>Topics & Sectors</h3>\r\n                <p>Participants are encouraged to submit proposals related to:</p>\r\n                <ul>\r\n                    <li><strong>Healthcare:</strong> AI diagnostics, predictive analytics, hospital operations</li>\r\n                    <li><strong>Aviation:</strong> Flight efficiency, predictive maintenance, air traffic control</li>\r\n                    <li><strong>Smart Cities:</strong> Traffic optimization, energy efficiency, public services</li>\r\n                    <li><strong>Cybersecurity:</strong> Threat detection, anomaly detection, security automation</li>\r\n                    <li><strong>Education:</strong> Personalized learning, automated assessments</li>\r\n                    <li><strong>Finance:</strong> Fraud detection, algorithmic trading</li>\r\n                    <li><strong>Energy:</strong> Consumption management, renewable optimization</li>\r\n                    <li><strong>Robotics:</strong> Industrial automation, intelligent systems</li>\r\n                </ul>\r\n                \r\n                <h3>Eligibility</h3>\r\n                <ul>\r\n                    <li>Open to all undergraduate students at Emirates Aviation University</li>\r\n                    <li>Teams of up to 2 members</li>\r\n                    <li>Individuals may participate in maximum 2 projects</li>\r\n                </ul>\r\n                \r\n                <h3>Support & Resources</h3>\r\n                <p>Shortlisted participants will receive:</p>\r\n                <ul>\r\n                    <li>Targeted workshops in Python, Excel, Power BI, and MATLAB</li>\r\n                    <li>Mentorship tailored to project requirements</li>\r\n                    <li>Technical resources to strengthen implementation</li>\r\n                </ul>\r\n                \r\n                <h3>Awards & Recognition</h3>\r\n                <ul>\r\n                    <li>Prizes for top 3 performing teams</li>\r\n                    <li>Certificates of participation for all Phase 2 participants</li>\r\n                    <li>Opportunity to be featured and nominated for top tech competitions</li>\r\n                </ul>\r\n            </div>\r\n        \r\n		\r\n		<div class=\"modal-footer\">\r\n		  <a \r\n			href=\"https://forms.office.com/Pages/DesignPageV2.aspx?prevorigin=shell&origin=NeoPortalPage&subpage=design&id=SmfvDn4j7kq73ntOIhN3n0CB9zCFMe5IrDTwQqCN9RhUQVJXWFhJT1UzRUk4SlUxM0YyT0ZHQlBQOS4u&analysis=true&tab=0\"\r\n			class=\"register-btn\"\r\n			target=\"_blank\" \r\n			rel=\"noopener noreferrer\"\r\n		  >\r\n			<svg viewBox=\"0 0 24 24\" width=\"20\" height=\"20\">\r\n			  <path fill=\"currentColor\" d=\"M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z\"/>\r\n			</svg>\r\n			Register Now\r\n		  </a>\r\n		</div>\r\n\r\n    </div>', '2025-05-16 09:47:38', '2025-05-16 09:49:36'),
(14, 'Robotics Workshop', 'Hands-on training sessions on robots fundamentals and advanced applications in aviation.', 'Coming Soon', 'Workshop', 'static/uploads/event_1747389088.865501_event2.png', '', '2025-05-16 09:51:28', '2025-05-16 09:51:28'),
(15, 'Project Pitch Days', 'Opportunity for students to present their innovative ideas to faculty and industry experts.', 'Coming Soon', 'Networking', 'static/uploads/event_1747389150.788218_event3.png', '', '2025-05-16 09:52:30', '2025-05-16 09:52:30'),
(16, 'Research Publication Bootcamp', 'Intensive training on academic writing and research paper publication strategies.', 'Coming Soon', 'Training', 'static/uploads/event_1747389233.131855_event4.png', '', '2025-05-16 09:53:30', '2025-05-16 09:53:53'),
(18, 'Testing', 'Input field and Word Test', 'September 15 , 2025', 'Competition', 'static/uploads/event_1749801096.993158_5.png', '<div class=\"modal-body\">\r\n    <h3>About the Challenge</h3>\r\n    <p>The Centre for Innovation in Robotics, Artificial Intelligence, Data Science, and Aviation (IRADA) at Emirates Aviation University is excited to announce <strong>EAU AIxplore 2025: IRADA Intra-University Innovation Challenge in AI, Data Science & Robotics</strong>—a prestigious platform for undergraduate students from various disciplines to demonstrate their creativity, problem-solving skills, and technical expertise.</p>\r\n    \r\n    <h3>Competition Structure</h3>\r\n    <p>The competition is structured in two phases:</p>\r\n    <ul>\r\n        <li><strong>Phase 1: Project Proposal Submission (April 30, 2025)</strong> - Submit proposals addressing key challenges in Data Science, AI, and Robotics across various sectors.</li>\r\n        <li><strong>Phase 2: Final Project Submission & Presentation (October 2, 2025)</strong> - Develop and present projects before expert judges.</li>\r\n    </ul>\r\n    \r\n    <h3>Topics & Sectors</h3>\r\n    <p>Participants are encouraged to submit proposals related to:</p>\r\n    <ul>\r\n        <li><strong>Healthcare:</strong> AI diagnostics, predictive analytics, hospital operations</li>\r\n        <li><strong>Aviation:</strong> Flight efficiency, predictive maintenance, air traffic control</li>\r\n        <li><strong>Smart Cities:</strong> Traffic optimization, energy efficiency, public services</li>\r\n        <li><strong>Cybersecurity:</strong> Threat detection, anomaly detection, security automation</li>\r\n        <li><strong>Education:</strong> Personalized learning, automated assessments</li>\r\n        <li><strong>Finance:</strong> Fraud detection, algorithmic trading</li>\r\n        <li><strong>Energy:</strong> Consumption management, renewable optimization</li>\r\n        <li><strong>Robotics:</strong> Industrial automation, intelligent systems</li>\r\n    </ul>\r\n    \r\n    <h3>Eligibility</h3>\r\n    <ul>\r\n        <li>Open to all undergraduate students at Emirates Aviation University</li>\r\n        <li>Teams of up to 2 members</li>\r\n        <li>Individuals may participate in maximum 2 projects</li>\r\n    </ul>\r\n    \r\n    <h3>Support & Resources</h3>\r\n    <p>Shortlisted participants will receive:</p>\r\n    <ul>\r\n        <li>Targeted workshops in Python, Excel, Power BI, and MATLAB</li>\r\n        <li>Mentorship tailored to project requirements</li>\r\n        <li>Technical resources to strengthen implementation</li>\r\n    </ul>\r\n    \r\n    <h3>Awards & Recognition</h3>\r\n    <ul>\r\n        <li>Prizes for top 3 performing teams</li>\r\n        <li>Certificates of participation for all Phase 2 participants</li>\r\n        <li>Opportunity to be featured and nominated for top tech competitions</li>\r\n    </ul>\r\n\r\n    <div class=\"registration-form\">\r\n        <h3>Registration Form</h3>\r\n        <form id=\"event2Registration\">\r\n            <div class=\"form-group\">\r\n                <label for=\"participantName\">Full Name:</label>\r\n                <input type=\"text\" id=\"participantName\" name=\"participantName\" required>\r\n            </div>\r\n            <div class=\"form-group\">\r\n                <label for=\"studentId\">Student ID:</label>\r\n                <input type=\"text\" id=\"studentId\" name=\"studentId\" required>\r\n            </div>\r\n            <div class=\"form-group\">\r\n                <label for=\"projectFile\">Upload Project Proposal (Word file):</label>\r\n                <input type=\"file\" id=\"projectFile\" name=\"projectFile\" accept=\".doc,.docx\" required>\r\n            </div>\r\n        </form>\r\n    </div>\r\n</div>\r\n\r\n<div class=\"modal-footer\">\r\n    <button type=\"submit\" form=\"event2Registration\" class=\"register-btn\">\r\n        <svg viewBox=\"0 0 24 24\" width=\"20\" height=\"20\">\r\n            <path fill=\"currentColor\" d=\"M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z\"/>\r\n        </svg>\r\n        Submit Registration\r\n    </button>\r\n</div>', '2025-06-13 07:51:36', '2025-06-13 07:51:36');

-- --------------------------------------------------------

--
-- Table structure for table `gallery_items`
--

CREATE TABLE `gallery_items` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `event_date` date NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `gallery_items`
--

INSERT INTO `gallery_items` (`id`, `title`, `event_date`, `image_path`, `created_at`) VALUES
(8, 'Event 1', '2025-05-13', 'static/uploads/gallery_1747387585.547796_1.png', '2025-05-16 09:26:25'),
(9, 'Event 2', '2025-07-27', 'static/uploads/gallery_1747387687.387543_2.png', '2025-05-16 09:28:07'),
(12, 'Event 3', '2025-06-10', 'static/uploads/gallery_1747388252.684921_6.png', '2025-05-16 09:37:32'),
(13, 'Event 4', '2025-08-13', 'static/uploads/gallery_1747388289.943203_5.png', '2025-05-16 09:38:09'),
(15, 'Event 5', '2025-08-20', 'static/uploads/gallery_1747388359.660627_8.png', '2025-05-16 09:39:19'),
(16, 'Event 6', '2025-10-23', 'static/uploads/gallery_1747388440.844697_img.png', '2025-05-16 09:40:40'),
(17, 'Event 7', '2025-11-19', 'static/uploads/gallery_1747388459.924926_event3.png', '2025-05-16 09:40:59'),
(18, 'Event 8', '2025-12-30', 'static/uploads/gallery_1747388500.557171_4.png', '2025-05-16 09:41:40'),
(19, 'Event 9', '2026-02-14', 'static/uploads/gallery_1747388547.236923_event3.png', '2025-05-16 09:42:27'),
(20, 'Event 10', '2026-07-14', 'static/uploads/gallery_1747388572.318823_event1.png', '2025-05-16 09:42:52'),
(21, 'Event 11', '2027-02-09', 'static/uploads/gallery_1747388594.238212_9.png', '2025-05-16 09:43:14'),
(23, 'ff', '2025-04-30', 'static/uploads/gallery_1747991471.245222_2.png', '2025-05-23 09:11:11');

-- --------------------------------------------------------

--
-- Table structure for table `ongoing_projects`
--

CREATE TABLE `ongoing_projects` (
  `id` int(11) NOT NULL,
  `project_title` varchar(255) NOT NULL,
  `domain` varchar(100) NOT NULL,
  `abstract` text NOT NULL,
  `researcher` varchar(100) NOT NULL,
  `supervisor` varchar(100) NOT NULL,
  `timeline` varchar(50) NOT NULL,
  `faculty` varchar(100) DEFAULT NULL,
  `programme` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ongoing_projects`
--

INSERT INTO `ongoing_projects` (`id`, `project_title`, `domain`, `abstract`, `researcher`, `supervisor`, `timeline`, `faculty`, `programme`, `created_at`, `updated_at`) VALUES
(3, 'AI-driven Text-to-Video Converter', 'AI & Machine Learning', 'This project develops an AI-powered Text-to-Video Converter that transforms text into engaging videos using NLP, GANs, and video synthesis, enabling scalable content creation for education, marketing, and public awareness.\r\n                    ', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', 'Short-term (0-3 months)', 'Faculty of Mathematics and Data Science', 'Bachelors of Science in Data Science', '2025-04-28 16:26:30', '2025-04-28 16:26:30'),
(4, 'Predictive Modelling for Sustainable Departures', 'Data Science', 'Air travel impacts CO₂ emissions, with peak-time departures causing delays and fuel waste. EcoDepart uses machine learning to analyze departure patterns, aiming to optimize schedules and promote sustainable aviation by reducing unnecessary emissions.\r\n                    ', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', 'Short-term (0-3 months)', 'Faculty of Mathematics and Data Science', 'Bachelors of Science in Software Engineering', '2025-04-28 16:32:35', '2025-04-28 16:32:35'),
(5, 'AI based Runway Incursion Prevention System', 'AI & Machine Learning', 'AI based Runway Incursion Prevention System AI based Runway Incursion Prevention System AI based Runway Incursion Prevention System AI based Runway Incursion Prevention System', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', 'Short-term (0-3 months)', 'Faculty of Mathematics and Dat Science', 'Bs Data Science', '2025-04-29 15:55:18', '2025-04-29 15:55:18'),
(6, '7 may', 'Data Science', 'Air travel impacts CO₂ emissions, with peak-time departures causing delays and fuel waste. EcoDepart uses machine learning to analyze departure patterns, aiming to optimize schedules and promote sustainable aviation by reducing unnecessary emissions. Air travel impacts CO₂ emissions, with peak-time.', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', 'Short-term (0-3 months)', 'Faculty of Engineering', 'Bs Data Science', '2025-05-07 10:44:40', '2025-05-07 10:44:40'),
(8, '26may_test5', 'AI & Machine Learning', '26may_test5', '26may_test5', 'Dr. Hannah Al Ali', 'Long-term (6+ months)', '26may_test5', '26may_test5', '2025-05-26 09:43:12', '2025-05-26 09:43:12'),
(9, '26may_test6', 'Robotics & Automation', '26may_test6', '26may_test6', 'Dr. Hannah Al Ali', 'Long-term (6+ months)', '26may_test6', '26may_test6', '2025-05-26 09:45:55', '2025-05-26 09:45:55'),
(10, '26may_test7', 'Data Science', '26may_test7', '26may_test7', 'Dr. Hannah Al Ali', 'Medium-term (3-6 months)', '26may_test7', '26may_test7', '2025-05-26 09:46:44', '2025-05-26 09:46:44');

-- --------------------------------------------------------

--
-- Table structure for table `project_proposals`
--

CREATE TABLE `project_proposals` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `project_title` varchar(255) NOT NULL,
  `project_brief` varchar(300) DEFAULT NULL,
  `team_members` text NOT NULL,
  `domain` varchar(255) DEFAULT NULL,
  `timeline` varchar(255) DEFAULT NULL,
  `needs_mentorship` tinyint(1) DEFAULT 0,
  `supervisor` varchar(255) DEFAULT NULL,
  `faculty` varchar(255) DEFAULT NULL,
  `programme` varchar(255) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `duration` varchar(50) DEFAULT NULL,
  `resources_required` text DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `submission_date` datetime NOT NULL,
  `status` enum('Accepted','Rejected','Pending') DEFAULT 'Pending',
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `project_proposals`
--

INSERT INTO `project_proposals` (`id`, `name`, `email`, `project_title`, `project_brief`, `team_members`, `domain`, `timeline`, `needs_mentorship`, `supervisor`, `faculty`, `programme`, `start_date`, `duration`, `resources_required`, `file_path`, `submission_date`, `status`, `user_id`) VALUES
(1, 'maham', 'maham@gmail.com', 'AI Image Generration', NULL, 'maham, fatima', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/proposal_form.pdf', '2025-04-07 09:22:09', 'Accepted', NULL),
(2, 'aylin', 'aylin@yahoo.com', 'Chatbot', NULL, 'anabia, aylin, mahnoor', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/IntroAI_Class_Exercise_03_02_2025__Lab1.docx', '2025-04-07 09:24:21', 'Rejected', NULL),
(3, 'saad', 'sad@s.com', 'Saad Project', NULL, 'Waleed, Umer', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/proposal_form.pdf', '2025-04-08 12:42:59', 'Rejected', NULL),
(4, 'Anum Meher', 'user4@gmail.com', 'Healcare Spealist', NULL, 'anum', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/IRADA_Intra-University_Innovation_Challenge_Brochure_Final_1.pdf', '2025-04-14 11:17:25', 'Pending', NULL),
(5, 'maham', 'maham@gmail.com', 'AI Image Generration', NULL, 'anabia, Waleed, bina', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/Exercices_1.docx', '2025-04-22 14:06:15', 'Pending', NULL),
(6, 'Azan', 'azaan@gmail.com', 'Azaan Project', NULL, 'Sharjeel, Saad', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/EAU_AIxplore_2025_Flyer_Layout.docx', '2025-04-22 14:08:08', 'Pending', NULL),
(7, 'Shahis', 'shahid@gmail.com', 'Shahid Project', NULL, 'Shahid, Kapoor', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/IntroAI_Class_Exercise_08_04_2025__Lab6.docx', '2025-04-22 14:14:23', 'Pending', NULL),
(8, 'test1', 'test1@gmail.com', 'test1 proj', NULL, 'team1, member 1', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/proposal_form.pdf', '2025-04-22 14:18:08', 'Pending', NULL),
(9, 'ayra', 'ayra@gmail.com', 'ayra proj', NULL, 'Ayra, Ahmed', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/MAF.docx', '2025-04-22 14:21:41', 'Pending', NULL),
(10, 'user2_try', 'user2@gmail.com', 'User2 Proj', NULL, '2 user', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/IntroAI_Class_Exercise_08_04_2025__Lab6_updated.docx', '2025-04-22 14:57:16', 'Accepted', NULL),
(11, 'User5', 'user5@gmail.com', 'user5proj', NULL, 'anaya', NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'uploads/proposal_form_5.pdf', '2025-04-24 12:57:12', 'Accepted', NULL),
(12, 'Kalsoom', 'kulsoom@gmail.com', 'Kulsoom Project', NULL, 'Kulsoom, Salahuddin', 'AI & Machine Learning', 'Short-term (0-3 months)', 0, 'Dr. Hannah Al Ali', 'Faculty of Engineering', 'Bs Data Science', NULL, NULL, NULL, 'uploads/IRADA_Intra-University_Innovation_Challenge_Brochure_Final_2.pdf', '2025-04-25 12:40:58', 'Accepted', NULL),
(13, 'Anya Ahmed', 'anya@gmail.com', 'Anya\'s Project', NULL, 'Anya Ahmed', 'Robotics & Automation', 'Long-term (6+ months)', 0, 'Maham Salahuddin', 'Faculty of Mathematics and Data Science', 'Bachelors of Science in Software Engineering', NULL, NULL, NULL, 'uploads/IRADA_Intra-University_Innovation_Challenge_Brochure_Final.pdf', '2025-05-02 09:20:58', 'Pending', NULL),
(14, '1145', '1145@gmail.com', '1145', NULL, '', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Deepudev Sahadevan', 'Faculty of Mathematics and Data Science', 'Bachelors of Science in Software Engineering', '2025-05-15', '3-6 months', 'PC, Nao, Other', 'uploads/IRADA_Intra-University_Innovation_Challenge_Brochure_Final_2.pdf', '2025-05-02 11:53:33', 'Pending', NULL),
(15, '12', '12@gmail.com', '12', NULL, '12', 'Data Science', 'Short-term (0-3 months)', 1, 'Dr. Deepudev Sahadevan', 'Faculty of Engineering', 'BS Software Engineering', '2025-05-30', NULL, 'PC, Other, 12', 'uploads/proposal_form_7.pdf', '2025-05-02 12:28:34', 'Pending', NULL),
(16, '2may', '2may@gmail.com', '2may', NULL, '2may', 'AI & Machine Learning', 'Medium-term (3-6 months)', 1, 'Dr. Deepudev Sahadevan', 'Faculty of Engineering', 'BS Software Engineering', '2025-05-09', NULL, 'Pepper, Other, terminus', 'uploads/proposal_form_7.pdf', '2025-05-02 12:54:49', 'Pending', NULL),
(17, 'test5', 'test5@gmail.com', 'test5', NULL, 'test5', 'Data Science', 'Medium-term (3-6 months)', 1, 'Dr. Deepudev Sahadevan', 'Faculty of Engineering', 'BS Software Engineering', '1111-12-01', NULL, 'Pepper, Other, test5', 'uploads/IRADA_Intra-University_Innovation_Challenge_in_AI_Data_Science__Robotics_1.pdf', '2025-05-02 12:56:59', 'Pending', NULL),
(18, '5may', '5may@gmail.com', '5may', NULL, '5may', 'Data Science', 'Short-term (0-3 months)', 1, 'Dr. Deepudev Sahadevan', 'Faculty of Mathematics and Dat Science', 'BS Software Engineering', '2025-04-29', NULL, 'PC, Other, fd', 'uploads/IRADA_Intra-University_Innovation_Challenge_Brochure_Final.pdf', '2025-05-05 11:18:41', 'Pending', NULL),
(19, '7 may ', 'user3@gmail.com', '7 May Project', 'Innovate.Discover.Transform. Aviation\'s Future, Today!  Accelerating Innovation in Artificial Intelligence, Robotics, Data Science, and Aviation” Background: Image collage of students, robots, data visualization, aircraft Innovate.Discover.Transform.Aviation\'s Future, Today!\r\nAccelerating Innovation', '', 'Robotics & Automation', 'Medium-term (3-6 months)', 1, 'Dr. Hannah Al Ali', '7 May ', '7 May', '2025-05-21', NULL, 'Pepper, Nao, Other, 7 May', 'uploads/proposal_form_13.pdf', '2025-05-07 11:30:14', 'Pending', NULL),
(20, 'test_test', 'test_test@gmail.com', 'test_test', 'test_test test_test test_test test_test test_test test_test test_testtest_test test_test test_test test_test test_test test_test test_test test_test test_test test_test test_test test_test test_test test_test test_test test_test test_test v vtest_test test_test test_test test_test v test_test test_t', 'test_test', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Deepudev Sahadevan', 'test_test', 'test_test', '2025-05-08', NULL, 'Pepper, Other, test_test', 'uploads/proposal_form_5.pdf', '2025-05-07 11:34:29', 'Pending', NULL),
(21, 'test_again', 'test_again@gmail.com', 'test_again', 'Artificial Intelligence (AI) is a groundbreaking technology shaping the future of industries and everyday life. From advanced robotics and self-driving cars to virtual assistants and personalised recommendations, AI is revolutionising the way we work, live, and interact. This page consists of essays', 'test_again', 'AI & Machine Learning', 'Long-term (6+ months)', 1, 'Dr. Deepudev Sahadevan', 'test_again', 'test_again', '2025-06-01', NULL, 'PC, High Performance PC + GPU, Other, test_again', 'uploads/proposal_form_6.pdf', '2025-05-07 11:46:38', 'Pending', NULL),
(22, 'trackcheck', 'trackcheck@gmail.com', 'trackcheck', 'trackcheck trackcheck trackcheck trackcheck trackcheck trackcheck trackcheck trackcheck trackcheck trackcheck trackcheck trackcheck trackcheck trackcheck ', 'trackcheck', 'Robotics & Automation', 'Medium-term (3-6 months)', 1, 'Dr. Hannah Al Ali', 'trackcheck', 'trackcheck', '2025-06-05', NULL, 'PC', 'uploads/proposal_form_6.pdf', '2025-05-07 12:01:02', 'Pending', NULL),
(23, 'user1_test', 'user1_test@gmail.com', 'user1_test', 'user1_test user1_test user1_test user1_test user1_test ', 'user1_test', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Deepudev Sahadevan', 'user1_test', 'user1_test', '2025-05-08', NULL, 'PC', 'uploads/EAU_AIxplore_2025_-_summary.docx', '2025-05-07 12:08:08', 'Pending', NULL),
(24, 'user3_test', 'deepudev@gmail.com', 'user3_test', 'user3_test user3_test user3_test', 'user3_test', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'user3_test', 'user3_test', '2025-05-30', NULL, 'PC', 'uploads/proposal_form_10.pdf', '2025-05-07 12:13:06', 'Pending', NULL),
(25, 'user3', 'user3@gmail.com', 'test_again', 'testing', 'test_test', 'AI & Machine Learning', 'Medium-term (3-6 months)', 1, 'Dr. Deepudev Sahadevan', 'test_test', 'test_test', '2025-05-17', NULL, 'PC', 'uploads/proposal_form_7.pdf', '2025-05-07 12:22:01', 'Pending', NULL),
(26, 'Anum Meher', 'maham@gmail.vom', 'Healcare Spealist', 'j s ckjnms kjc sbjk mslbj sjb avkoj; x m', '7 May', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'user3_test', 'test_test', '2025-05-01', NULL, 'Pepper', 'uploads/IRADA_Intra-University_Innovation_Challenge_in_AI_Data_Science__Robotics_1.pdf', '2025-05-07 12:34:20', 'Pending', NULL),
(27, 'az', 'maham.salah002@gmail.com', 'ad', 'ad', 'dax', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Deepudev Sahadevan', 'ad', 'd', '2025-05-19', NULL, 'PC, Other, d', 'uploads/cmd.docx', '2025-05-07 14:19:28', 'Pending', NULL),
(28, 'plz yar', 'user1_test@gmail.com', 'plz yar', 'plz yar plz yar plz yar', 'plz yar', 'AI & Machine Learning', 'Medium-term (3-6 months)', 1, 'Dr. Deepudev Sahadevan', 'plz yar', 'plz yar', '2025-05-22', NULL, 'PC, Other, plz yar', 'uploads/EAU_AIxplore_2025_-_summary.docx', '2025-05-07 14:44:51', 'Pending', NULL),
(29, 'user1_plz', 'user1_test@gmail.com', 'user1_plz', 'user1_plz user1_plz user1_plz', 'user1_plz', 'AI & Machine Learning', 'Medium-term (3-6 months)', 1, 'Dr. Hannah Al Ali', 'user1_plz', 'user1_plz', '2025-05-31', NULL, 'PC, Other, user1_plz', 'uploads/EAU_AIxplore_2025_-_summary.docx', '2025-05-07 14:51:52', 'Pending', NULL),
(30, '12may', '12@gmail.com', '12may', '12may 12may 12may', '12may', 'Robotics & Automation', 'Medium-term (3-6 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Mathematics and Dat Science', 'check', '2025-05-24', NULL, 'PC', 'uploads/proposal_form_9.pdf', '2025-05-12 12:58:16', 'Pending', NULL),
(31, 'check_99', 'fafs@vf.f', 'check_99', 'check_99', 'f', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'check_99', 'check_99', '2025-05-16', NULL, 'PC, Pepper, Other, check_99', 'uploads/cmd.docx', '2025-05-12 16:46:26', 'Pending', NULL),
(32, 'check_99', 'check_99@d.c', 'check_99', 'check_99', 'check_99', 'Robotics & Automation', 'Medium-term (3-6 months)', 1, 'Dr. Deepudev Sahadevan', 'check_99', 'check_99', '2025-05-30', NULL, 'PC, Other, check_99', 'uploads/cmd.docx', '2025-05-12 16:47:40', 'Pending', NULL),
(33, 'check_99', 'check_99v@d.c', 'check)999', 'check)999', 'check)999', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'check)999', 'check)999', '2025-05-05', NULL, 'Other, sc', 'uploads/cmd.docx', '2025-05-12 16:57:27', 'Pending', NULL),
(34, 'maham_check_user', '1145@gmail.com', 'maham_check_user', 'maham_check_user maham_check_user', 'maham_check_user', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'maham_check_user', 'maham_check_user', '2025-05-21', NULL, 'PC, High Performance PC + GPU, Other, maham_check_user', 'uploads/proposal_form_14.pdf', '2025-05-13 09:37:26', 'Pending', 3),
(35, 'rrr', 'check_99@d.c', 'rrr', 'rrr', 'rrr', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'rrr', 'rrr', '2025-05-16', NULL, 'PC, Pepper, Other, rrr', 'uploads/cmd.docx', '2025-05-13 09:49:59', 'Pending', 3),
(36, 'ajeeb', 'ajeeb@e.v', 'ajeeb', 'ajeeb', 'ef', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'ajeeb', 'ajeeb', '2025-05-23', NULL, 'PC, Other, d', 'uploads/cmd.docx', '2025-05-13 11:13:02', 'Accepted', 3),
(37, 'user1 submission', 'check_99@d.c', 'user1 submission', 'user1 submission user1 submission user1 submission user1 submission', 'user1 submission ', 'AI & Machine Learning', 'Medium-term (3-6 months)', 1, 'Dr. Hannah Al Ali', 'user1 submission', 'user1 submission', '2025-05-03', NULL, 'High Performance PC + GPU, Nao, Other, user1 submission', 'uploads/cmd.docx', '2025-05-13 11:33:07', 'Pending', 2),
(38, 'User 1 Test', 'User@1.com', 'User 1 Test', 'User 1 Test User 1 Test User 1 Test User 1 Test User 1 Test User 1 Test User 1 Test User 1 Test User 1 Test', 'User 1 Test', 'AI & Machine Learning', 'Medium-term (3-6 months)', 1, 'Dr. Hannah Al Ali', 'User 1 Test', 'User 1 Test', '2025-05-09', NULL, 'PC, Other, User 1 Test', 'uploads/cmd.docx', '2025-05-13 15:57:14', 'Pending', 2),
(39, 'Test 15 may', 'check999@gmail.vom', 'Test 15 may', 'Test 15 may', 'Test 15 may', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Test 15 may', 'Test 15 may', '2025-05-18', NULL, 'PC', 'static/proposal_form_9.pdf', '2025-05-15 13:41:48', 'Accepted', 2),
(40, 'User2_20may', '20may@em.c', 'User2_20may', 'User2_20may', 'User2_20may', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Other', 'Other', '2025-05-17', NULL, 'PC, Nao', 'static/proposal_form_11.pdf', '2025-05-20 14:43:30', 'Pending', 3),
(41, 'Anna', 'anna@gmail.om', 'Chatbot', 'aaa', 'aa', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Business Management', 'Extended Diploma in Aviation Operations', '2025-05-17', NULL, 'PC', 'static/proposal_form_8.pdf', '2025-05-21 16:27:10', 'Pending', 3),
(42, 'Maham Salahuddin', 'maham@gmail.com', 'AI based Runway Incursion Prevention System', 'An Autonomous Runway Incursion Warning System (ARIWS) is a system which provides autonomous detection of a potential incursion or of the occupancy of an active runway and a direct warning to a flight crew or a vehicle operator (ICAO).', 'Maham ', 'AI & Machine Learning', 'Medium-term (3-6 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Mathematics and Data Science', '', '2025-05-10', NULL, 'PC, Nao', 'static/cmd.docx', '2025-05-22 14:15:22', 'Pending', 7),
(43, 'check_23may', 'maham@gmail.com', 'check_23may', 'check_23may', 'check_23may', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Professional Training', 'Dispatch Resource Management (DRM)', '2025-05-15', NULL, 'PC, Other, check_23may', 'static/proposal_form_16.pdf', '2025-05-23 09:03:35', 'Pending', 3),
(44, '22may_10am', 'maham@gmail.com', '22may_10am', '22may_10am', '22may_10am', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Mathematics and Data Science', 'Bachelor of Science in Data Science', '2025-05-16', NULL, 'PC, Other, 22may_10am', 'static/cmd.docx', '2025-05-23 10:20:07', 'Pending', 3),
(45, '22may_10am', 'fafs@vf.f', '22may_10am', '22may_10am', '22may_10am, 22may_10am', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'The Postgraduate Centre', 'Postgraduate Certificate in Aerospace Engineering', '2025-05-25', NULL, '', 'static/cmd.docx', '2025-05-23 10:21:10', 'Pending', 3),
(46, '22may_10am1', 'fafs@vf.f', '22may_10am1', '22may_10am1', '22may_10am1', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Engineering', 'Bachelor of Engineering (Hons) in Aerospace Technology', '2025-05-22', NULL, 'PC', 'static/cmd.docx', '2025-05-23 10:23:57', 'Pending', 3),
(47, '22may_10am2', 'maham.salah002@gmail.com', '22may_10am2', '22may_10am2', '', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Professional Training', 'Flight Dispatch (FDIC)', '2025-05-23', NULL, '', 'static/cmd.docx', '2025-05-23 10:33:52', 'Pending', 3),
(48, '22may_10am3', 'fafs@vf.f', 'check_99', '22may_10am3', '22may_10am3', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Mathematics and Data Science', 'BSc (Hons) in Computer Science with Artificial Intelligence', '2025-05-13', NULL, 'Pepper', 'static/cmd.docx', '2025-05-23 10:37:47', 'Pending', 3),
(49, '22may_10am4', 'maham.salah002@gmail.com', '22may_10am3', '22may_10am3', '22may_10am3', 'Robotics & Automation', 'Medium-term (3-6 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Engineering', 'Higher Diploma in Aircraft Maintenance Engineering', '2025-05-30', NULL, 'PC', 'static/cmd.docx', '2025-05-23 10:39:09', 'Pending', 3),
(50, 'required', 'required@e.m', 'required', 'required', '', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Engineering', 'Bachelor of Engineering (Hons) in Applied Mechanical Engineering', '2025-05-22', NULL, 'PC', 'static/cmd.docx', '2025-05-23 10:48:26', 'Pending', 3),
(51, 'required1', 'required@e.m', 'required', 'required', 'required', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Engineering', 'Bachelor of Engineering (Hons) in Applied Mechanical Engineering', '2025-05-06', NULL, 'PC', 'static/cmd.docx', '2025-05-23 10:49:28', 'Pending', 3),
(52, '22may', '22may@e.d', '22may', '22may', '22may', 'Robotics & Automation', 'Short-term (0-3 months)', 0, NULL, 'Faculty of Engineering', 'Extended Diploma in Aeronautical Engineering', '2025-04-29', NULL, 'PC', 'static/cmd.docx', '2025-05-23 10:57:12', 'Pending', 5),
(53, '22may1', '22may@e.d', '22may1', '22may1', 'a, b', 'Data Science', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Faculty of Mathematics and Data Science', 'Bachelor of Science in Software Engineering', '2025-05-26', NULL, 'Nao, Other, 22may', 'static/cmd.docx', '2025-05-23 10:57:56', 'Pending', 5),
(54, 'saad', '12@gmail.com', 'saad1', 'saad1', 'saad1', 'Data Science', 'Medium-term (3-6 months)', 1, 'Dr. Thomas Mgonja', 'Faculty of Mathematics and Data Science', 'BSc (Hons) in Computer Science with Artificial Intelligence', '2025-05-15', NULL, 'PC', 'static/cmd.docx', '2025-05-23 13:22:06', 'Pending', 19),
(55, 'anya_test1', 'anya_test1@g.m', 'anya_test1', 'anya_test1', 'anya_test1', 'Data Science', 'Short-term (0-3 months)', 0, NULL, 'Professional Training', 'Flight Dispatch (FDIC)', '2025-05-15', NULL, 'PC', 'static/cmd.docx', '2025-05-23 13:27:57', 'Pending', 19),
(56, 'anya_test2', 'anya_test1@g.m', 'anya_test2', 'anya_test2', 'anya_test2, 2, 3', 'Robotics & Automation', 'Medium-term (3-6 months)', 1, 'Prof. Hannah Al Ali', 'Faculty of Engineering', 'Bachelor of Science in Aeronautical Engineering', '2025-05-14', NULL, 'PC', 'static/cmd.docx', '2025-05-23 13:28:58', 'Pending', 19),
(57, 'anya_test3', 'anya@gmail.com', 'anya_test3', 'anya_test3', 'a, v, d, d', 'Data Science', 'Medium-term (3-6 months)', 1, 'Prof. Hannah Al Ali', 'Faculty of Mathematics and Data Science', '', '2025-05-13', NULL, 'PC, Other, anya_test3', 'static/cmd.docx', '2025-05-23 13:30:24', 'Pending', 19),
(58, 'anya_test4', 'anya@gmail.com', 'anya_test4', 'anya_test4', 'anya_test4', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Mawada Nasser', 'Professional Training', 'Flight Dispatch Recurrent Course (FDRC)', '2025-05-22', NULL, '', 'static/cmd.docx', '2025-05-23 13:31:11', 'Pending', 19),
(59, 'supervisor_check', 'supervisor_check@gmail.com', 'supervisor_check', 'supervisor_check', 'supervisor_check', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'dr-mostafa', 'Faculty of Mathematics and Data Science', 'Bachelor of Science in Computer Science', '2025-05-08', NULL, 'PC, Other, supervisor_check', 'static/cmd.docx', '2025-05-23 13:52:05', 'Pending', 19),
(60, 'Saba', 'saba@gmail.com', 'PROJECT1', 'PROJECT1 ', 'SABA', 'Robotics & Automation', 'Long-term (6+ months)', 1, 'dr-zaytoon', 'Faculty of Mathematics and Data Science', 'Bachelor of Science in Data Science', '2025-05-29', NULL, 'Simulation Tool, Nao, Other, resource_name', 'static/cmd.docx', '2025-05-23 15:12:50', 'Accepted', 23),
(61, 'Maham', 'eg1@gmail.com', 'Smart Vision', 'Project Brief ..............', 'Maham', 'AI & Machine Learning', 'Short-term (0-3 months)', 1, 'dr-muner', 'Faculty of Mathematics and Data Science', 'Bachelor of Science in Data Science', '2025-05-24', NULL, 'High Performance PC + GPU', 'static/cmd.docx', '2025-05-23 15:29:40', 'Rejected', 23),
(62, 'Aylin', 'eg2@gmail.com', 'Adaptive Intelligence', 'Project Brief...........', 'Aylin ', 'Robotics & Automation', 'Long-term (6+ months)', 0, NULL, 'Professional Training', 'International Aviation Management Conference', '2025-05-14', NULL, 'High Performance PC + GPU, Simulation Tool', 'static/cmd.docx', '2025-05-23 15:30:55', 'Pending', 23),
(63, 'Lara', 'lara@gmail.com', 'AI-based Chatbot', 'An AI chatbot is a software application that uses artificial intelligence to simulate human conversations. ', 'Lara', 'Data Science', 'Long-term (6+ months)', 1, 'dr-rukshanda', 'Faculty of Engineering', 'Bachelor of Engineering (Hons) in Avionics Technology', '2025-05-26', NULL, 'High Performance PC + GPU', 'static/cmd.docx', '2025-05-26 11:13:34', 'Pending', 23),
(64, '26_may', 'user3@gmail.com', '26_may', '26_may', '26_may', 'Robotics & Automation', 'Medium-term (3-6 months)', 1, 'dr-yacob', 'Faculty of Mathematics and Data Science', 'BSc (Hons) in Data Science', '2025-05-30', NULL, 'PC, Nao', 'static/proposal_form_9.pdf', '2025-05-26 12:07:29', 'Pending', 5),
(65, '13June', '13june@gmail.com', '13june', '13june', '13june', 'AI & Machine Learning', 'Medium-term (3-6 months)', 1, 'dr-mahmoud', 'Other', 'Other', '2025-06-17', NULL, 'PC, Other, 13june', 'static/cmd.docx', '2025-06-13 10:15:52', 'Pending', 3),
(66, '13june_update1', '13june_update1@g.s', '13june_update1', '13june_update1', '13june_update1', 'AI & Machine Learning', 'Medium-term (3-6 months)', 1, 'riham-arab', '13june_update1', '13june_update1', '2025-06-04', NULL, 'PC, Other, 13june_update1', 'static/cmd.docx', '2025-06-13 10:33:46', 'Pending', 3);

-- --------------------------------------------------------

--
-- Table structure for table `resource_requests`
--

CREATE TABLE `resource_requests` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `project_id` int(11) DEFAULT NULL,
  `project_id1` int(11) DEFAULT NULL,
  `purpose` text DEFAULT NULL,
  `hardware_resources` text DEFAULT NULL,
  `software_resources` text DEFAULT NULL,
  `lab_area` varchar(100) DEFAULT NULL,
  `needs_mentorship` tinyint(1) DEFAULT 0,
  `mentor_name` varchar(100) DEFAULT NULL,
  `request_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `justification` text NOT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `admin_response` text DEFAULT NULL,
  `submission_date` datetime DEFAULT current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `resource_requests`
--

INSERT INTO `resource_requests` (`id`, `user_id`, `project_id`, `project_id1`, `purpose`, `hardware_resources`, `software_resources`, `lab_area`, `needs_mentorship`, `mentor_name`, `request_date`, `start_time`, `end_time`, `justification`, `status`, `admin_response`, `submission_date`, `created_at`) VALUES
(1, 5, NULL, NULL, 'axdxa', NULL, 'MATLAB,PyTorch,Other,wdz', NULL, 1, 'da', '2025-05-09', '10:49:00', '12:49:00', 'dfszf', 'pending', NULL, '2025-05-06 09:50:08', '2025-05-06 10:46:44'),
(2, 3, NULL, NULL, 'sda', 'PC,High Performance PC + GPU', NULL, NULL, 1, 'wd', '2025-05-01', '15:17:00', '14:17:00', 'dw', 'approved', '', '2025-05-06 12:17:48', '2025-05-06 10:46:44'),
(3, 3, NULL, NULL, 'sda', 'PC,High Performance PC + GPU', NULL, NULL, 1, 'wd', '2025-05-01', '15:17:00', '14:17:00', 'dw', 'pending', NULL, '2025-05-06 12:19:53', '2025-05-06 10:46:44'),
(4, 3, NULL, NULL, 'sda', 'PC,High Performance PC + GPU', NULL, NULL, 1, 'wd', '2025-05-01', '15:17:00', '14:17:00', 'dw', 'pending', NULL, '2025-05-06 12:20:03', '2025-05-06 10:46:44'),
(5, 3, NULL, NULL, 'zzz', 'PC,High Performance PC + GPU', NULL, NULL, 1, 'zz', '2025-05-09', '05:57:00', '16:57:00', 'zzz', 'pending', NULL, '2025-05-06 12:57:57', '2025-05-06 10:46:44'),
(6, 3, NULL, NULL, 'xxxx', NULL, NULL, 'Data Science Lab', 1, 'xxxx', '2025-05-23', '13:11:00', '14:11:00', 'xxxx', 'pending', NULL, '2025-05-06 13:11:15', '2025-05-06 10:46:44'),
(7, 2, NULL, NULL, 'user1_test1', NULL, 'MATLAB,TensorFlow,Other,user1_test1', NULL, 1, 'user1_test1', '2025-05-22', '05:22:00', '15:20:00', 'user1_test1', 'pending', NULL, '2025-05-06 13:18:39', '2025-05-06 10:46:44'),
(8, 3, NULL, NULL, 'user2_test1', NULL, 'MATLAB,TensorFlow,PyTorch,Other,user2_test1', NULL, 1, 'user2_test1', '2025-05-23', '13:26:00', '02:20:00', 'user2_test1', 'rejected', 'it is busy', '2025-05-06 13:20:42', '2025-05-06 10:46:44'),
(9, 6, NULL, NULL, 'test1_user4', NULL, NULL, NULL, 1, 'test1_user4', '2025-05-17', '08:55:00', '16:55:00', 'test1_user4', 'pending', NULL, '2025-05-06 14:55:28', '2025-05-06 10:55:28'),
(10, 3, NULL, NULL, 'test2_2', NULL, NULL, NULL, 1, 'test2_2', '2025-05-16', '08:59:00', '15:59:00', 'test2_2', 'pending', NULL, '2025-05-06 14:59:23', '2025-05-06 10:59:23'),
(11, 3, NULL, NULL, '6may', 'PC,Pepper', 'MATLAB,Choregraphe', 'Robotics Lab', 1, '6may', '2025-05-07', '07:48:00', '13:54:00', '6may', 'pending', NULL, '2025-05-07 07:48:35', '2025-05-07 03:48:35'),
(12, 3, NULL, NULL, '6may-test1', 'PC,Pepper,6may-test1', 'MATLAB,PyTorch,6may-test1', NULL, 1, '6may-test1', '2025-05-31', '13:00:00', '14:00:00', '6may-test1', 'approved', '', '2025-05-07 07:50:29', '2025-05-07 03:50:29'),
(13, 3, NULL, NULL, 'check', 'check', 'PyTorch,check', 'Robotics Lab', 1, 'check', '2025-05-01', '10:01:00', '11:01:00', 'check', 'pending', NULL, '2025-05-07 08:41:39', '2025-05-07 04:41:39'),
(14, 3, NULL, NULL, 'hello', 'PC,Pepper,hello', 'MATLAB,TensorFlow,hello', NULL, 0, NULL, '2025-06-07', '13:01:00', '14:20:00', 'hello', 'rejected', 'Resources are allocated alreday at that time. Request for another time please', '2025-05-07 10:15:52', '2025-05-07 06:15:52'),
(15, 3, NULL, NULL, 'hello2', 'hello2', NULL, NULL, 1, 'hello2', '2025-05-18', '01:20:00', '01:20:00', 'hello2 ', 'pending', NULL, '2025-05-07 10:16:51', '2025-05-07 06:16:51'),
(16, 2, NULL, NULL, 'row 1 check', 'PC,row 1 check', NULL, NULL, 1, 'row 1 check', '2025-06-07', '10:26:00', '02:21:00', 'row 1 check', 'pending', NULL, '2025-05-07 10:21:07', '2025-05-07 06:21:07'),
(17, 2, NULL, NULL, 'row 2 check', 'High Performance PC + GPU,row 2 check', 'MATLAB', NULL, 1, 'row 2 check', '2025-05-02', '10:21:00', '00:21:00', 'row 2 check', 'pending', NULL, '2025-05-07 10:21:35', '2025-05-07 06:21:35'),
(18, 2, NULL, NULL, 'row 3 check', 'Pepper', 'Python IDEs', 'Robotics Lab', 0, NULL, '2025-06-06', '10:24:00', '11:22:00', 'row 3 check', 'rejected', '', '2025-05-07 10:22:14', '2025-05-07 06:22:14'),
(19, 2, NULL, NULL, 'row 4 check', 'Pepper', NULL, 'AI Research Lab', 1, 'row 4 check', '2025-05-29', '22:28:00', '10:26:00', 'row 4 check', 'pending', NULL, '2025-05-07 10:22:43', '2025-05-07 06:22:43'),
(20, 2, NULL, NULL, 'row 5 check', NULL, NULL, 'Robotics Lab', 1, 'row 5 check', '2025-05-31', '10:26:00', '10:29:00', 'row 5 check', 'rejected', '', '2025-05-07 10:23:07', '2025-05-07 06:23:07'),
(21, 3, NULL, NULL, 'xyz ', 'PC,Pepper', 'Python IDEs,PyTorch', NULL, 1, 'rrr', '2025-05-02', '11:09:00', '13:09:00', 'rrrrrrrrrrrrrrrrrrrrrrrrr ', 'pending', NULL, '2025-05-14 15:09:46', '2025-05-14 11:09:46'),
(22, 3, NULL, NULL, 'check_23may', 'PC', NULL, NULL, 1, 'check_23may', '2025-05-14', '10:05:00', '01:05:00', 'check_23may', 'pending', NULL, '2025-05-23 09:05:05', '2025-05-23 05:05:05'),
(23, 3, NULL, NULL, 'check_23may1', 'PC', NULL, NULL, 1, 'check_23may1', '2025-05-09', '10:05:00', '13:05:00', 'check_23may1', 'pending', NULL, '2025-05-23 09:05:49', '2025-05-23 05:05:49'),
(24, 3, NULL, NULL, 'check_23may2', 'PC,Nao,check_23may2', 'MATLAB,Python IDEs,check_23may2', 'IRADA Innovation Center', 1, 'check_23may2', '2025-05-07', '10:06:00', '13:06:00', 'check_23may2', 'pending', NULL, '2025-05-23 09:06:32', '2025-05-23 05:06:32'),
(25, 3, NULL, NULL, '23may_test', 'PC', NULL, NULL, 1, '6may-test1', '2025-05-08', '09:19:00', '12:19:00', '23may_test', 'pending', NULL, '2025-05-23 09:19:20', '2025-05-23 05:19:20'),
(26, 3, NULL, NULL, 'f', 'PC', NULL, NULL, 1, 'test2_2', '2025-05-14', '09:21:00', '11:21:00', 'test2_2', 'pending', NULL, '2025-05-23 09:22:09', '2025-05-23 05:22:09'),
(27, 3, 2, NULL, NULL, 'PC', NULL, NULL, 1, '22may_test4', '2025-05-28', '11:36:00', '13:36:00', '22may_test4', 'pending', NULL, '2025-05-23 09:36:51', '2025-05-23 05:36:51'),
(28, 3, 5, NULL, NULL, 'PC', 'Python IDEs', 'PHD Lab 1', 1, '22may_test5', '2025-05-23', '01:38:00', '11:38:00', '22may_test5', 'pending', NULL, '2025-05-23 09:38:25', '2025-05-23 05:38:25'),
(29, 3, 4, NULL, NULL, 'PC', NULL, NULL, 1, '2may_test6', '2025-05-29', '09:43:00', '09:44:00', '2may_test6', 'approved', '', '2025-05-23 09:39:38', '2025-05-23 05:39:38'),
(30, 3, NULL, NULL, '22may_7', 'Nao', NULL, NULL, 1, '22may_7', '2025-05-08', '21:51:00', '09:51:00', '22may_7', 'pending', NULL, '2025-05-23 09:51:34', '2025-05-23 05:51:34'),
(31, 3, 3, NULL, NULL, 'High Performance PC + GPU', NULL, NULL, 1, '22may_8', '2025-05-22', '09:52:00', '21:52:00', '22may_8', 'pending', NULL, '2025-05-23 09:52:07', '2025-05-23 05:52:07'),
(32, 3, NULL, NULL, '22may_9', NULL, 'Python IDEs', NULL, 1, '22may_9', '2025-05-15', '09:56:00', '21:56:00', '22may_9', 'pending', NULL, '2025-05-23 09:56:48', '2025-05-23 05:56:48'),
(33, 3, NULL, NULL, '22may_test10', 'PC', NULL, NULL, 1, '22may_test10', '2025-05-16', '01:01:00', '02:01:00', '22may_test10', 'pending', NULL, '2025-05-23 10:01:19', '2025-05-23 06:01:19'),
(34, 3, NULL, NULL, '22may_test11', NULL, NULL, NULL, 1, '22may_test10', '2025-05-07', '10:03:00', '01:01:00', '22may_test10', 'pending', NULL, '2025-05-23 10:02:01', '2025-05-23 06:02:01'),
(35, 3, NULL, NULL, 'o', NULL, 'Python IDEs', NULL, 0, NULL, '2025-05-28', '10:02:00', '22:02:00', '22may_test12', 'approved', '', '2025-05-23 10:03:06', '2025-05-23 06:03:06'),
(36, 3, 6, NULL, NULL, '', NULL, NULL, 1, '22may_13', '2025-05-03', '10:06:00', '22:06:00', '22may_13', 'pending', NULL, '2025-05-23 10:06:27', '2025-05-23 06:06:27'),
(37, 3, 2, NULL, NULL, 'High Performance PC + GPU', NULL, NULL, 1, '', '2025-05-14', '01:21:00', '10:25:00', '22may_10am', 'pending', NULL, '2025-05-23 10:21:50', '2025-05-23 06:21:50'),
(38, 19, 4, NULL, NULL, 'Simulation Tool', 'Python IDEs,TensorFlow', '', 1, 'S', '2025-05-09', '17:23:00', '13:28:00', 'a', 'approved', '', '2025-05-23 13:23:18', '2025-05-23 09:23:18'),
(39, 23, 3, NULL, NULL, 'PC,High Performance PC + GPU', NULL, NULL, 1, 'Dr Muhammad', '2025-05-15', '09:13:00', '16:13:00', 'xxxx', 'pending', NULL, '2025-05-23 15:13:50', '2025-05-23 11:13:50'),
(40, 23, NULL, NULL, 'Real-Time Object Detection', 'PC,High Performance PC + GPU,Nao', 'Python IDEs,Choregraphe', 'IRADA Innovation Center', 1, 'Dr Fatima', '2025-05-10', '00:16:00', '16:25:00', ' Papper and PC are required to deploy a computer vision model for real-time object detection and tracking in robotics.', 'pending', NULL, '2025-05-23 15:19:40', '2025-05-23 11:19:40'),
(41, 23, NULL, NULL, 'Autonomous Navigation', 'PC', 'Python IDEs,ROS', NULL, 1, 'Dr Khalid', '2025-06-04', '07:20:00', '09:20:00', 'Access to lab and software like ROS is necessary to simulate autonomous navigation and SLAM with AI-based path planning.', 'pending', NULL, '2025-05-23 15:21:04', '2025-05-23 11:21:04'),
(42, 23, NULL, NULL, 'Smart Interaction System ', 'PC,High Performance PC + GPU,Pepper', 'Choregraphe', NULL, 0, NULL, '2025-06-04', '08:22:00', '09:22:00', 'I need access to a high-performance PC for training deep learning models, and Pepper for deploying and testing real-world HRI (human-robot interaction) scenarios.', 'rejected', 'Plz request for another time in afternoon. Resources are already allocated in the morning', '2025-05-23 15:22:17', '2025-05-23 11:22:17'),
(43, 23, NULL, NULL, 'Humanoid Motion in Nao', 'PC,Nao', 'Choregraphe', 'IRADA Innovation Center', 0, NULL, '2025-06-27', '12:22:00', '14:25:00', 'I need access to a high-performance PC for training deep learning models, and Pepper for deploying and testing real-world HRI (human-robot interaction) scenarios.', 'approved', '', '2025-05-23 15:23:09', '2025-05-23 11:23:09'),
(44, 23, NULL, NULL, 'a', '', '', '', 1, '', '2025-05-16', '08:32:00', '20:32:00', 'a', 'pending', NULL, '2025-05-26 08:32:19', '2025-05-26 04:32:19'),
(45, 23, NULL, NULL, 'aa', NULL, NULL, NULL, 0, NULL, '2025-05-10', '11:32:00', '20:36:00', 'aa', 'pending', NULL, '2025-05-26 08:32:42', '2025-05-26 04:32:42'),
(46, 3, NULL, NULL, 's', 'PC', NULL, NULL, 1, 's', '2025-05-22', '21:18:00', '09:18:00', 's', 'pending', NULL, '2025-05-26 09:15:22', '2025-05-26 05:15:22'),
(47, 3, NULL, NULL, 'w', 'PC', NULL, NULL, 1, 'w', '2025-05-14', '00:18:00', '01:18:00', 'w', 'pending', NULL, '2025-05-26 09:18:09', '2025-05-26 05:18:09'),
(48, 3, NULL, NULL, 'check_26may', 'PC', NULL, NULL, 1, 'check_26may', '2025-05-07', '09:26:00', '11:23:00', 'check_26may', 'pending', NULL, '2025-05-26 09:23:53', '2025-05-26 05:23:53'),
(49, 3, 4, NULL, NULL, 'PC', NULL, NULL, 1, 'g', '2025-05-09', '09:31:00', '11:29:00', 'g', 'pending', NULL, '2025-05-26 09:29:05', '2025-05-26 05:29:05'),
(50, 3, 3, NULL, NULL, 'Pepper', NULL, NULL, 1, 'Video Converter', '2025-05-29', '01:31:00', '01:31:00', 'Video Converter', 'pending', NULL, '2025-05-26 09:31:05', '2025-05-26 05:31:05'),
(51, 3, 3, NULL, NULL, NULL, NULL, NULL, 1, '26may_test1', '2025-05-21', '01:35:00', '02:35:00', '26may_test1', 'pending', NULL, '2025-05-26 09:35:08', '2025-05-26 05:35:08'),
(52, 3, 4, NULL, NULL, NULL, NULL, NULL, 1, '26may_test2', '2025-05-08', '09:38:00', '11:35:00', '26may_test2', 'pending', NULL, '2025-05-26 09:36:11', '2025-05-26 05:36:11'),
(53, 3, 5, NULL, NULL, NULL, NULL, NULL, 1, '26may_test3', '2025-05-23', '01:37:00', '02:37:00', '26may_test3', 'pending', NULL, '2025-05-26 09:37:09', '2025-05-26 05:37:09'),
(54, 3, 6, NULL, NULL, NULL, NULL, NULL, 1, '26may_test4', '2025-05-30', '11:37:00', '02:37:00', '26may_test4', 'pending', NULL, '2025-05-26 09:37:56', '2025-05-26 05:37:56'),
(55, 3, 8, NULL, NULL, NULL, NULL, NULL, 1, '26may_test5', '2025-05-10', '09:46:00', '09:45:00', '26may_test5', 'pending', NULL, '2025-05-26 09:43:41', '2025-05-26 05:43:41'),
(56, 3, 10, NULL, NULL, NULL, NULL, NULL, 1, '26may_test7', '2025-05-21', '09:51:00', '09:51:00', '26may_test7', 'pending', NULL, '2025-05-26 09:48:46', '2025-05-26 05:48:46'),
(57, 3, NULL, 3, NULL, NULL, NULL, NULL, 1, 'af_test1', '2025-05-29', '10:18:00', '10:18:00', 'af_test1', 'pending', NULL, '2025-05-26 10:14:51', '2025-05-26 06:14:51'),
(58, 24, NULL, 3, NULL, 'PC,Nao', NULL, NULL, 1, 'test1', '2025-05-07', '10:20:00', '00:17:00', 'test1', 'pending', NULL, '2025-05-26 10:17:19', '2025-05-26 06:17:19'),
(59, 24, NULL, 6, NULL, 'Pepper', 'Python IDEs', 'IRADA Innovation Center', 1, 'test_2', '2025-05-28', '10:21:00', '10:20:00', 'test_2', 'rejected', 'mm', '2025-05-26 10:17:53', '2025-05-26 06:17:53'),
(60, 24, NULL, 4, NULL, 'Nao,test3', 'TensorFlow,test3', NULL, 1, 'test3', '2025-05-15', '11:50:00', '00:50:00', 'test3', 'approved', '', '2025-05-26 10:18:50', '2025-05-26 06:18:50'),
(61, 24, NULL, NULL, 'Test4', 'Simulation Tool', NULL, NULL, 1, 'Test4', '2025-05-28', '02:24:00', '02:24:00', 'Test4', 'pending', NULL, '2025-05-26 10:24:57', '2025-05-26 06:24:57'),
(62, 23, NULL, 5, NULL, 'High Performance PC + GPU', 'Python IDEs,PyTorch', NULL, 1, 'Dr. Mohsin', '2025-06-12', '11:14:00', '14:14:00', 'I want to work on my project', 'approved', '', '2025-05-26 11:15:29', '2025-05-26 07:15:29');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','user') NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`) VALUES
(1, 'admin', 'admin@temp.com', 'scrypt:32768:8:1$pKafUJ6Rqel4DXCZ$8173c7225afaff6146b5a0d516de38b0e0b804ef783fe1a480ae53b02a7640340f9d5fbd51ab0ce13711e1fc0940459093c673e6e7ab482d928673d6c15622d5', 'admin'),
(2, 'user1', 'user1@temp.com', 'scrypt:32768:8:1$2876gj5IsFNWgPqU$78182f62a6f9167385084c755673cca8860426dfb4345808a440d3ac586ca31cd9842c5c4b67837fbfee966bd59905e6610180c85f1f51a67d55938f8abd4c85', 'user'),
(3, 'user2', 'user2@temp.com', 'scrypt:32768:8:1$scH4DREwkQVxXUaq$c86cd29dacd42ec6318ee6092d19c2bf1a5cae0129a196ddd444c2405ca62d6ed6ad116e7e7aa9363fcb1ee42525dd1b5f4b62900a7b1eebc3ba1e4d53caae45', 'user'),
(5, 'user3', 'user3@temp.com', 'scrypt:32768:8:1$fXWfCWxoBombhd3z$4e0daccf5f83d4831443e727c83d8950cdf2cf210033a8fd14986794054d0bf4b5fa6774e83d60cb6c673e5ea66aa2d8ff5ed59f6691843602b979f147838cd9', 'user'),
(6, 'user4', 'user4@temp.com', 'scrypt:32768:8:1$Wo11cR6X09AZGkPf$5d4399499f7c23553a0c9adbf0a554ae14d2a81007607a27c4a46e717ebfbc950fa1a13a42768b2be1cae9362dffffcea176ab077fcc51c620d2a709d8b5263e', 'user'),
(7, 'maham', 'maham@gmail.com', 'scrypt:32768:8:1$YgRdj4Co0aUaP4mN$bee88255a49bdf412eda78ba7d72a468bed4c5e5db07e874743c962537ce2880bc736879f19dbfc66f34d6e3dcdc933b0f426532fc16866d785cb82de026592d', 'user'),
(10, 'maham1', 'maham1@gmail.com', 'scrypt:32768:8:1$izMCHLoZAl7id68p$62a803f821adfe38f7dc7f4a15203e21d62059801523f499d70b36fcd1eee6d41056aeb75603e1ffd222beb244454242dacc08a6458cef695db23fce34ce7405', 'user'),
(11, 'user10', 'user10@gmail.com', 'scrypt:32768:8:1$GsH44cK179KAP0t1$660e899ddb0b35459a01bef0c1a39671e09ccabf372d4feedce104dc996652863af88077ddd7dfe2d8fc0d3ef31321a04aae3abfb8e9486703bf36bc437053fe', 'user'),
(13, 'testcase1', 'testcase1@eau.ac.ae', 'scrypt:32768:8:1$obpKces9RfOuOuDF$350f286c3465f074c799f13998d7422abd2bbf50c5f19a40f4e9fa052456b2b4e5f89db2ded6f1ffd97bbf39b204256b82713fd54684503caa13ddad398c869b', 'user'),
(16, 'testcase122', 'testcase122@eau.ac.ae', 'scrypt:32768:8:1$eWXCZH33q4CKdHat$52462d28693a10f68ecbbb3968039be625f56beed3f62c3b1e534f99698375f8a753d0ee8d48059ab047070199762c7f26f37ec92f37bc3a57add54e9e009478', 'user'),
(18, 'user5', 'user5@gmail.com', 'scrypt:32768:8:1$TUkWbSYxHZMjvBPw$4c97d21646a3fda9e7e15739b09e276d9e0d2245933ad2963b6ccf22ff3163eb12736417721acc498a5803febcf8f28d95ecb08a048ddf2f9f5dc04567b890d4', 'user'),
(19, 'anya', 'anya@gmail.com', 'scrypt:32768:8:1$yiwfkqS8atUIkJNR$b6cf18783a279c590783216a5fa9300c3dab93bfafc59c855306ecb039fb3c5c29b09bbaac3c83cda3889cbc648ed4f1aacc74483549335c6597f4895fb88509', 'user'),
(21, 'fatima', 'fatima@gmail.com', 'scrypt:32768:8:1$WhTnABGZPpqcA0fg$11a79b0fa2f4bb9684995c603bf4f2b3e3ad13dd652c86b678da97da872716bd1eb96f37b5b7403bec3160df063a09f0e8dedc4d19bd8dfa8c45bfab96ed9b26', 'user'),
(22, 'user6', 'user6@gmail.com', 'scrypt:32768:8:1$EeJcG6FyZ4HBizWy$a6eae0f9e929daf95cfe9eb0d947bb98b14ae938ec150a711534bdd65aa306fae6f4f4c60de17fccf50d7955dc5191b8d015fa93744c2cf0c5684e82ce7c3598', 'user'),
(23, 'irada', 'irada@gmail.com', 'scrypt:32768:8:1$JJOAFgVZubbbRLwZ$d3d496b81df395ecb399c245e9cc5030dd21aaab034fa2a8f777c83c7f481b7dc2942d87a48c13be566e9ff75113ebee3d5389de3cb97746612c56c988eef09d', 'user'),
(24, 'test_resource', 'test_resource@gmail.com', 'scrypt:32768:8:1$f61AKnIRVCLN5MZA$715f0eef46736a3c9930296402ff1d3c3396e521352dbda3afe9fcf63545536e1dd2a1596d74f14afb6a5de7cf85d96bd4ed711d590faede1f1bf1ab9f1229f6', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `completed_projects`
--
ALTER TABLE `completed_projects`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `gallery_items`
--
ALTER TABLE `gallery_items`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ongoing_projects`
--
ALTER TABLE `ongoing_projects`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `project_proposals`
--
ALTER TABLE `project_proposals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- Indexes for table `resource_requests`
--
ALTER TABLE `resource_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `project_id` (`project_id`),
  ADD KEY `resource_requests_ibfk_3` (`user_id`),
  ADD KEY `resource_requests_ibfk_4` (`project_id1`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `completed_projects`
--
ALTER TABLE `completed_projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `gallery_items`
--
ALTER TABLE `gallery_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `ongoing_projects`
--
ALTER TABLE `ongoing_projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `project_proposals`
--
ALTER TABLE `project_proposals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT for table `resource_requests`
--
ALTER TABLE `resource_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `project_proposals`
--
ALTER TABLE `project_proposals`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `resource_requests`
--
ALTER TABLE `resource_requests`
  ADD CONSTRAINT `resource_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `resource_requests_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project_proposals` (`id`),
  ADD CONSTRAINT `resource_requests_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `resource_requests_ibfk_4` FOREIGN KEY (`project_id1`) REFERENCES `ongoing_projects` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

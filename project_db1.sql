-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 15, 2025 at 12:45 PM
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
(7, 'Test 15 may', 'Robotics & Automation', 'Test 15 may TST ', 'Test 15 may', 'Dr. Hannah Al Ali', '2025-05-15', 'static\\poster_1747302219.328131_maham.jpeg', 'static\\video_1747302219.328131_Project_Title_-_001_Demo_Video.mp4', 'static\\report_1747302219.329128_report_1745904781.528683_IntroAI_Class_Exercise_08_04_2025__Lab6.docx', 'Test 15 may', 'Test 15 may', '2025-05-15 09:43:39');

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
(1, 'Event 1', 'Event 1 will be held for undergrdaude students ', 'May 15 - May 17', 'Competition', 'uploads/event_1747281713.239679_poster_1745904957.467991_nao.png', 'Event 1 will be held for undergrdaude students  Event 1 will be held for undergrdaude students  Event 1 will be held for undergrdaude students  Event 1 will be held for undergrdaude students  Event 1 will be held for undergrdaude students ', '2025-05-15 04:01:53', '2025-05-15 04:01:53'),
(2, 'Event 2 ', 'Event 2 will be held for undergrdaude students Event 1 will be held for undergrdaude students', 'June 15 - May 17', 'Competition', 'uploads/event_1747282284.283441_poster_1745905534.064162_1.png', '', '2025-05-15 04:11:24', '2025-05-15 04:11:24'),
(3, '\\Event 3 ', 'Event 3 will be held for undergrdaude students Event 3 will be held for undergrdaude students', 'August 15 , 2025', 'Competition', 'uploads/event_1747282352.298631_event_1747282284.283441_poster_1745905534.064162_1.png', '', '2025-05-15 04:12:32', '2025-05-15 04:12:32'),
(4, 'Event 4', 'Event 4 will be held for undergrdaude students Event 4 will be held for undergrdaude students', 'September 15 , 2025', 'Competition', 'static/uploads/event_1747301503.672925_event2.png', 'Event 3 will be held for undergrdaude students Event 3 will be held for undergrdaude students', '2025-05-15 09:31:05', '2025-05-15 09:31:43'),
(5, 'Event 5', 'sdh djh lhin zklm,  k,zhmdhi ', 'June 15 - May 17', 'Workshop', 'static/event_1747301599.091322_event3.png', '', '2025-05-15 09:33:19', '2025-05-15 09:33:19'),
(6, 'Test', 'Test 1 Test 1 Test 1 Test 1 Test 1 Test 1 Test 1 Test 1 Test 1 Test 1 ', 'June 15 - May 17', 'Competition', 'static/event_1747301862.733963_event4.png', '', '2025-05-15 09:37:42', '2025-05-15 09:37:42'),
(7, 'Test 2 ', 'Test Test 2 ', 'September 15 , 2025', 'Competition', 'static/uploads/event_1747301970.290076_event4.png', '', '2025-05-15 09:39:30', '2025-05-15 09:39:30'),
(8, 'AI Explore- Data Science Competiton', ' AI Explore- Data Science Competiton is for passionate studentrs who wants to have exposure of technology and innovation. ', '15 May 2025', 'Competition', 'static/uploads/event_1747304430.644523_4.png', '<h1> What is data science?\r\n<p> Data science combines math and statistics, specialized programming, advanced analytics, artificial intelligence (AI) and machine learning with specific subject matter expertise to uncover actionable insights hidden in an organization’s data. These insights can be used to guide decision making and strategic planning. </p> \r\n\r\n<h2> Data Science Lifecycle </h2>\r\n\r\n<p>The data science lifecycle involves various roles, tools, and processes, which enables analysts to glean actionable insights. Typically, a data science project undergoes the following stages:</p>\r\n\r\n<ul>\r\n  <li>Data ingestion: The lifecycle begins with the data collection, both raw structured and unstructured data from all relevant sources using a variety of methods. These methods can include manual entry, web scraping, and real-time streaming data from systems and devices. Data sources can include structured data, such as customer data, along with unstructured data like log files, video, audio, pictures, the Internet of Things (IoT), social media, and more.</li>\r\n  <li>Data storage and data processing: Since data can have different formats and structures, companies need to consider different storage systems based on the type of data that needs to be captured. Data management teams help to set standards around data storage and structure, which facilitate workflows around analytics, machine learning and deep learning models. This stage includes cleaning data, deduplicating, transforming and combining the data using ETL (extract, transform, load) jobs or other data integration technologies. This data preparation is essential for promoting data quality before loading into a data warehouse, data lake, or other repository.</li>\r\n  <li>Data analysis: Here, data scientists conduct an exploratory data analysis to examine biases, patterns, ranges, and distributions of values within the data. This data analytics exploration drives hypothesis generation for a/b testing. It also allows analysts to determine the data’s relevance for use within modeling efforts for predictive analytics, machine learning, and/or deep learning. Depending on a model’s accuracy, organizations can become reliant on these insights for business decision making, allowing them to drive more scalability.</li>\r\n</ul>\r\n\r\n\r\n\r\n', '2025-05-15 10:20:30', '2025-05-15 10:20:30'),
(9, 'Test AI xplore ', 'AI Explore TEST- Data Science Competiton is for passionate studentrs who wants to have exposure of technology and innovation. ', 'September 15 , 2025', 'Competition', 'static/uploads/event_1747304714.1404_img.png', '<h1>EAU AIxplore 2025: IRADA Intra-University Innovation Challenge </h1>\r\n\r\n <h3>About the Challenge</h3>\r\n                <p>The Centre for Innovation in Robotics, Artificial Intelligence, Data Science, and Aviation (IRADA) at Emirates Aviation University is excited to announce <strong>EAU AIxplore 2025: IRADA Intra-University Innovation Challenge in AI, Data Science & Robotics</strong>—a prestigious platform for undergraduate students from various disciplines to demonstrate their creativity, problem-solving skills, and technical expertise.</p>\r\n                \r\n                <h3>Competition Structure</h3>\r\n                <p>The competition is structured in two phases:</p>\r\n                <ul>\r\n                    <li><strong>Phase 1: Project Proposal Submission (April 30, 2025)</strong> - Submit proposals addressing key challenges in Data Science, AI, and Robotics across various sectors.</li>\r\n                    <li><strong>Phase 2: Final Project Submission & Presentation (October 2, 2025)</strong> - Develop and present projects before expert judges.</li>\r\n                </ul>\r\n                \r\n                <h3>Topics & Sectors</h3>\r\n                <p>Participants are encouraged to submit proposals related to:</p>\r\n                <ul>\r\n                    <li><strong>Healthcare:</strong> AI diagnostics, predictive analytics, hospital operations</li>\r\n                    <li><strong>Aviation:</strong> Flight efficiency, predictive maintenance, air traffic control</li>\r\n                    <li><strong>Smart Cities:</strong> Traffic optimization, energy efficiency, public services</li>\r\n                    <li><strong>Cybersecurity:</strong> Threat detection, anomaly detection, security automation</li>\r\n                    <li><strong>Education:</strong> Personalized learning, automated assessments</li>\r\n                    <li><strong>Finance:</strong> Fraud detection, algorithmic trading</li>\r\n                    <li><strong>Energy:</strong> Consumption management, renewable optimization</li>\r\n                    <li><strong>Robotics:</strong> Industrial automation, intelligent systems</li>\r\n                </ul>\r\n                \r\n                <h3>Eligibility</h3>\r\n                <ul>\r\n                    <li>Open to all undergraduate students at Emirates Aviation University</li>\r\n                    <li>Teams of up to 2 members</li>\r\n                    <li>Individuals may participate in maximum 2 projects</li>\r\n                </ul>\r\n                \r\n                <h3>Support & Resources</h3>\r\n                <p>Shortlisted participants will receive:</p>\r\n                <ul>\r\n                    <li>Targeted workshops in Python, Excel, Power BI, and MATLAB</li>\r\n                    <li>Mentorship tailored to project requirements</li>\r\n                    <li>Technical resources to strengthen implementation</li>\r\n                </ul>\r\n                \r\n                <h3>Awards & Recognition</h3>\r\n                <ul>\r\n                    <li>Prizes for top 3 performing teams</li>\r\n                    <li>Certificates of participation for all Phase 2 participants</li>\r\n                    <li>Opportunity to be featured and nominated for top tech competitions</li>\r\n                </ul>\r\n<div class=\"modal-footer\">\r\n		  <a \r\n			href=\"https://forms.office.com/Pages/DesignPageV2.aspx?prevorigin=shell&origin=NeoPortalPage&subpage=design&id=SmfvDn4j7kq73ntOIhN3n0CB9zCFMe5IrDTwQqCN9RhUQVJXWFhJT1UzRUk4SlUxM0YyT0ZHQlBQOS4u&analysis=true&tab=0\"\r\n			class=\"register-btn\"\r\n			target=\"_blank\" \r\n			rel=\"noopener noreferrer\"\r\n		  >\r\n			<svg viewBox=\"0 0 24 24\" width=\"20\" height=\"20\">\r\n			  <path fill=\"currentColor\" d=\"M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z\"/>\r\n			</svg>\r\n			Register Now\r\n		  </a>\r\n		</div>', '2025-05-15 10:25:14', '2025-05-15 10:25:14'),
(10, 'Data Science', 'The event is about data sciuence and how it is evolving', 'June 15 - May 17', 'Workshop', 'static/uploads/event_1747304874.294722_6.png', '\r\n            <div class=\"modal-header\">\r\n                <h2>EAU AIxplore 2025: IRADA Intra-University Innovation Challenge</h2>\r\n                <div class=\"modal-meta\">\r\n                    <div class=\"modal-date\">\r\n                        <svg viewBox=\"0 0 24 24\">\r\n                            <path d=\"M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM9 10H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm-8 4H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2z\"/>\r\n                        </svg>\r\n                        April 30 - October 2, 2025\r\n                    </div>\r\n                    <div class=\"modal-location\">\r\n                        <svg viewBox=\"0 0 24 24\">\r\n                            <path d=\"M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z\"/>\r\n                        </svg>\r\n                        Emirates Aviation University\r\n                    </div>\r\n                    <div class=\"modal-deadline\">\r\n                        <svg viewBox=\"0 0 24 24\">\r\n                            <path d=\"M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z\"/>\r\n                        </svg>\r\n                        Registration Deadline: April 30, 2025\r\n                    </div>\r\n                </div>\r\n            </div>\r\n            <div class=\"modal-body\">\r\n                <h3>About the Challenge</h3>\r\n                <p>The Centre for Innovation in Robotics, Artificial Intelligence, Data Science, and Aviation (IRADA) at Emirates Aviation University is excited to announce <strong>EAU AIxplore 2025: IRADA Intra-University Innovation Challenge in AI, Data Science & Robotics</strong>—a prestigious platform for undergraduate students from various disciplines to demonstrate their creativity, problem-solving skills, and technical expertise.</p>\r\n                \r\n                <h3>Competition Structure</h3>\r\n                <p>The competition is structured in two phases:</p>\r\n                <ul>\r\n                    <li><strong>Phase 1: Project Proposal Submission (April 30, 2025)</strong> - Submit proposals addressing key challenges in Data Science, AI, and Robotics across various sectors.</li>\r\n                    <li><strong>Phase 2: Final Project Submission & Presentation (October 2, 2025)</strong> - Develop and present projects before expert judges.</li>\r\n                </ul>\r\n                \r\n                <h3>Topics & Sectors</h3>\r\n                <p>Participants are encouraged to submit proposals related to:</p>\r\n                <ul>\r\n                    <li><strong>Healthcare:</strong> AI diagnostics, predictive analytics, hospital operations</li>\r\n                    <li><strong>Aviation:</strong> Flight efficiency, predictive maintenance, air traffic control</li>\r\n                    <li><strong>Smart Cities:</strong> Traffic optimization, energy efficiency, public services</li>\r\n                    <li><strong>Cybersecurity:</strong> Threat detection, anomaly detection, security automation</li>\r\n                    <li><strong>Education:</strong> Personalized learning, automated assessments</li>\r\n                    <li><strong>Finance:</strong> Fraud detection, algorithmic trading</li>\r\n                    <li><strong>Energy:</strong> Consumption management, renewable optimization</li>\r\n                    <li><strong>Robotics:</strong> Industrial automation, intelligent systems</li>\r\n                </ul>\r\n                \r\n                <h3>Eligibility</h3>\r\n                <ul>\r\n                    <li>Open to all undergraduate students at Emirates Aviation University</li>\r\n                    <li>Teams of up to 2 members</li>\r\n                    <li>Individuals may participate in maximum 2 projects</li>\r\n                </ul>\r\n                \r\n                <h3>Support & Resources</h3>\r\n                <p>Shortlisted participants will receive:</p>\r\n                <ul>\r\n                    <li>Targeted workshops in Python, Excel, Power BI, and MATLAB</li>\r\n                    <li>Mentorship tailored to project requirements</li>\r\n                    <li>Technical resources to strengthen implementation</li>\r\n                </ul>\r\n                \r\n                <h3>Awards & Recognition</h3>\r\n                <ul>\r\n                    <li>Prizes for top 3 performing teams</li>\r\n                    <li>Certificates of participation for all Phase 2 participants</li>\r\n                    <li>Opportunity to be featured and nominated for top tech competitions</li>\r\n                </ul>\r\n            </div>\r\n        \r\n		\r\n		<div class=\"modal-footer\">\r\n		  <a \r\n			href=\"https://forms.office.com/Pages/DesignPageV2.aspx?prevorigin=shell&origin=NeoPortalPage&subpage=design&id=SmfvDn4j7kq73ntOIhN3n0CB9zCFMe5IrDTwQqCN9RhUQVJXWFhJT1UzRUk4SlUxM0YyT0ZHQlBQOS4u&analysis=true&tab=0\"\r\n			class=\"register-btn\"\r\n			target=\"_blank\" \r\n			rel=\"noopener noreferrer\"\r\n		  >\r\n			<svg viewBox=\"0 0 24 24\" width=\"20\" height=\"20\">\r\n			  <path fill=\"currentColor\" d=\"M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z\"/>\r\n			</svg>\r\n			Register Now\r\n		  </a>\r\n		</div>\r\n\r\n    </div>', '2025-05-15 10:27:54', '2025-05-15 10:29:26');

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
(2, 'Ongoing proj 2', 'Data Science', 'Ongoing proj 2 Ongoing proj 2 Ongoing proj 2 Ongoing proj 2Ongoing proj 2 Ongoing proj 2', 'Kulsoom Salahuddin', 'Dr. Hannah Al Ali', 'Medium-term (3-6 months)', 'Faculty of Engineering', 'Bs Data Science', '2025-04-28 12:04:02', '2025-04-28 12:04:02'),
(3, 'AI-driven Text-to-Video Converter', 'AI & Machine Learning', 'This project develops an AI-powered Text-to-Video Converter that transforms text into engaging videos using NLP, GANs, and video synthesis, enabling scalable content creation for education, marketing, and public awareness.\r\n                    ', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', 'Short-term (0-3 months)', 'Faculty of Mathematics and Data Science', 'Bachelors of Science in Data Science', '2025-04-28 16:26:30', '2025-04-28 16:26:30'),
(4, 'Predictive Modelling for Sustainable Departures', 'Data Science', 'Air travel impacts CO₂ emissions, with peak-time departures causing delays and fuel waste. EcoDepart uses machine learning to analyze departure patterns, aiming to optimize schedules and promote sustainable aviation by reducing unnecessary emissions.\r\n                    ', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', 'Short-term (0-3 months)', 'Faculty of Mathematics and Data Science', 'Bachelors of Science in Software Engineering', '2025-04-28 16:32:35', '2025-04-28 16:32:35'),
(5, 'AI based Runway Incursion Prevention System', 'AI & Machine Learning', 'AI based Runway Incursion Prevention System AI based Runway Incursion Prevention System AI based Runway Incursion Prevention System AI based Runway Incursion Prevention System', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', 'Short-term (0-3 months)', 'Faculty of Mathematics and Dat Science', 'Bs Data Science', '2025-04-29 15:55:18', '2025-04-29 15:55:18'),
(6, '7 may', 'Data Science', 'Air travel impacts CO₂ emissions, with peak-time departures causing delays and fuel waste. EcoDepart uses machine learning to analyze departure patterns, aiming to optimize schedules and promote sustainable aviation by reducing unnecessary emissions. Air travel impacts CO₂ emissions, with peak-time.', 'Maham Salahuddin', 'Dr. Deepudev Sahadevan', 'Short-term (0-3 months)', 'Faculty of Engineering', 'Bs Data Science', '2025-05-07 10:44:40', '2025-05-07 10:44:40');

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
(39, 'Test 15 may', 'check999@gmail.vom', 'Test 15 may', 'Test 15 may', 'Test 15 may', 'Robotics & Automation', 'Short-term (0-3 months)', 1, 'Dr. Hannah Al Ali', 'Test 15 may', 'Test 15 may', '2025-05-18', NULL, 'PC', 'static/proposal_form_9.pdf', '2025-05-15 13:41:48', 'Accepted', 2);

-- --------------------------------------------------------

--
-- Table structure for table `resource_requests`
--

CREATE TABLE `resource_requests` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `project_id` int(11) DEFAULT NULL,
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

INSERT INTO `resource_requests` (`id`, `user_id`, `project_id`, `purpose`, `hardware_resources`, `software_resources`, `lab_area`, `needs_mentorship`, `mentor_name`, `request_date`, `start_time`, `end_time`, `justification`, `status`, `admin_response`, `submission_date`, `created_at`) VALUES
(1, 5, NULL, 'axdxa', NULL, 'MATLAB,PyTorch,Other,wdz', NULL, 1, 'da', '2025-05-09', '10:49:00', '12:49:00', 'dfszf', 'pending', NULL, '2025-05-06 09:50:08', '2025-05-06 10:46:44'),
(2, 3, NULL, 'sda', 'PC,High Performance PC + GPU', NULL, NULL, 1, 'wd', '2025-05-01', '15:17:00', '14:17:00', 'dw', 'approved', '', '2025-05-06 12:17:48', '2025-05-06 10:46:44'),
(3, 3, NULL, 'sda', 'PC,High Performance PC + GPU', NULL, NULL, 1, 'wd', '2025-05-01', '15:17:00', '14:17:00', 'dw', 'pending', NULL, '2025-05-06 12:19:53', '2025-05-06 10:46:44'),
(4, 3, NULL, 'sda', 'PC,High Performance PC + GPU', NULL, NULL, 1, 'wd', '2025-05-01', '15:17:00', '14:17:00', 'dw', 'pending', NULL, '2025-05-06 12:20:03', '2025-05-06 10:46:44'),
(5, 3, NULL, 'zzz', 'PC,High Performance PC + GPU', NULL, NULL, 1, 'zz', '2025-05-09', '05:57:00', '16:57:00', 'zzz', 'pending', NULL, '2025-05-06 12:57:57', '2025-05-06 10:46:44'),
(6, 3, NULL, 'xxxx', NULL, NULL, 'Data Science Lab', 1, 'xxxx', '2025-05-23', '13:11:00', '14:11:00', 'xxxx', 'pending', NULL, '2025-05-06 13:11:15', '2025-05-06 10:46:44'),
(7, 2, NULL, 'user1_test1', NULL, 'MATLAB,TensorFlow,Other,user1_test1', NULL, 1, 'user1_test1', '2025-05-22', '05:22:00', '15:20:00', 'user1_test1', 'pending', NULL, '2025-05-06 13:18:39', '2025-05-06 10:46:44'),
(8, 3, NULL, 'user2_test1', NULL, 'MATLAB,TensorFlow,PyTorch,Other,user2_test1', NULL, 1, 'user2_test1', '2025-05-23', '13:26:00', '02:20:00', 'user2_test1', 'rejected', 'it is busy', '2025-05-06 13:20:42', '2025-05-06 10:46:44'),
(9, 6, NULL, 'test1_user4', NULL, NULL, NULL, 1, 'test1_user4', '2025-05-17', '08:55:00', '16:55:00', 'test1_user4', 'pending', NULL, '2025-05-06 14:55:28', '2025-05-06 10:55:28'),
(10, 3, NULL, 'test2_2', NULL, NULL, NULL, 1, 'test2_2', '2025-05-16', '08:59:00', '15:59:00', 'test2_2', 'pending', NULL, '2025-05-06 14:59:23', '2025-05-06 10:59:23'),
(11, 3, NULL, '6may', 'PC,Pepper', 'MATLAB,Choregraphe', 'Robotics Lab', 1, '6may', '2025-05-07', '07:48:00', '13:54:00', '6may', 'pending', NULL, '2025-05-07 07:48:35', '2025-05-07 03:48:35'),
(12, 3, NULL, '6may-test1', 'PC,Pepper,6may-test1', 'MATLAB,PyTorch,6may-test1', NULL, 1, '6may-test1', '2025-05-31', '13:00:00', '14:00:00', '6may-test1', 'approved', '', '2025-05-07 07:50:29', '2025-05-07 03:50:29'),
(13, 3, NULL, 'check', 'check', 'PyTorch,check', 'Robotics Lab', 1, 'check', '2025-05-01', '10:01:00', '11:01:00', 'check', 'pending', NULL, '2025-05-07 08:41:39', '2025-05-07 04:41:39'),
(14, 3, NULL, 'hello', 'PC,Pepper,hello', 'MATLAB,TensorFlow,hello', NULL, 0, NULL, '2025-06-07', '13:01:00', '14:20:00', 'hello', 'pending', NULL, '2025-05-07 10:15:52', '2025-05-07 06:15:52'),
(15, 3, NULL, 'hello2', 'hello2', NULL, NULL, 1, 'hello2', '2025-05-18', '01:20:00', '01:20:00', 'hello2 ', 'pending', NULL, '2025-05-07 10:16:51', '2025-05-07 06:16:51'),
(16, 2, NULL, 'row 1 check', 'PC,row 1 check', NULL, NULL, 1, 'row 1 check', '2025-06-07', '10:26:00', '02:21:00', 'row 1 check', 'pending', NULL, '2025-05-07 10:21:07', '2025-05-07 06:21:07'),
(17, 2, NULL, 'row 2 check', 'High Performance PC + GPU,row 2 check', 'MATLAB', NULL, 1, 'row 2 check', '2025-05-02', '10:21:00', '00:21:00', 'row 2 check', 'pending', NULL, '2025-05-07 10:21:35', '2025-05-07 06:21:35'),
(18, 2, NULL, 'row 3 check', 'Pepper', 'Python IDEs', 'Robotics Lab', 0, NULL, '2025-06-06', '10:24:00', '11:22:00', 'row 3 check', 'rejected', '', '2025-05-07 10:22:14', '2025-05-07 06:22:14'),
(19, 2, NULL, 'row 4 check', 'Pepper', NULL, 'AI Research Lab', 1, 'row 4 check', '2025-05-29', '22:28:00', '10:26:00', 'row 4 check', 'pending', NULL, '2025-05-07 10:22:43', '2025-05-07 06:22:43'),
(20, 2, NULL, 'row 5 check', NULL, NULL, 'Robotics Lab', 1, 'row 5 check', '2025-05-31', '10:26:00', '10:29:00', 'row 5 check', 'rejected', '', '2025-05-07 10:23:07', '2025-05-07 06:23:07'),
(21, 3, NULL, 'xyz ', 'PC,Pepper', 'Python IDEs,PyTorch', NULL, 1, 'rrr', '2025-05-02', '11:09:00', '13:09:00', 'rrrrrrrrrrrrrrrrrrrrrrrrr ', 'pending', NULL, '2025-05-14 15:09:46', '2025-05-14 11:09:46');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','user') NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `role`) VALUES
(1, 'admin', 'scrypt:32768:8:1$pKafUJ6Rqel4DXCZ$8173c7225afaff6146b5a0d516de38b0e0b804ef783fe1a480ae53b02a7640340f9d5fbd51ab0ce13711e1fc0940459093c673e6e7ab482d928673d6c15622d5', 'admin'),
(2, 'user1', 'scrypt:32768:8:1$2876gj5IsFNWgPqU$78182f62a6f9167385084c755673cca8860426dfb4345808a440d3ac586ca31cd9842c5c4b67837fbfee966bd59905e6610180c85f1f51a67d55938f8abd4c85', 'user'),
(3, 'user2', 'scrypt:32768:8:1$scH4DREwkQVxXUaq$c86cd29dacd42ec6318ee6092d19c2bf1a5cae0129a196ddd444c2405ca62d6ed6ad116e7e7aa9363fcb1ee42525dd1b5f4b62900a7b1eebc3ba1e4d53caae45', 'user'),
(5, 'user3', 'scrypt:32768:8:1$fXWfCWxoBombhd3z$4e0daccf5f83d4831443e727c83d8950cdf2cf210033a8fd14986794054d0bf4b5fa6774e83d60cb6c673e5ea66aa2d8ff5ed59f6691843602b979f147838cd9', 'user'),
(6, 'user4', 'scrypt:32768:8:1$Wo11cR6X09AZGkPf$5d4399499f7c23553a0c9adbf0a554ae14d2a81007607a27c4a46e717ebfbc950fa1a13a42768b2be1cae9362dffffcea176ab077fcc51c620d2a709d8b5263e', 'user');

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
  ADD KEY `user_id` (`user_id`),
  ADD KEY `project_id` (`project_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `completed_projects`
--
ALTER TABLE `completed_projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `ongoing_projects`
--
ALTER TABLE `ongoing_projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `project_proposals`
--
ALTER TABLE `project_proposals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `resource_requests`
--
ALTER TABLE `resource_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

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
  ADD CONSTRAINT `resource_requests_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project_proposals` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

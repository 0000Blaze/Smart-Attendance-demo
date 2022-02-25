<?php session_start(); ?>
<html>

<head>
    <title>Departments</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <link rel="stylesheet" href="../css/departStyle.css">
</head>
<body>
      <?php
    include 'connectToDb.php';

    if (!$sqldb->select_db('sas')) 
    {
        die("not connected to database");
    }
    $startDate = $_POST["startDate"];
    $endDate = $_POST["endDate"];
    $subject = $_POST["subject"];

    // echo $startDate;
    // echo $endDate;
    // echo $subject;
    $getAttendanceQuery ="SELECT aID FROM attendance WHERE scode = '$subject' AND DATE(time) >= '$startdate' AND DATE(time) <= '$enddate'";

?>
</body>
</html>
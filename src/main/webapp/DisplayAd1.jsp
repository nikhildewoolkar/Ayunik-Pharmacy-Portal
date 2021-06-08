<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Insert title here</title>

</head>
<body>
<%@page import="java.util.ArrayList"%>      <%--Importing all the dependent classes--%>
<%@page import="com.SwapTreasure.app.*"%>
<%@page import="java.util.Iterator"%> 

<%
 	ArrayList<Artifacts> ad = (ArrayList) request.getAttribute("treasures");
 %> <%--Assigning ArrayList object containing Employee data to the local object --%>

<strong><a href="<%=request.getContextPath()%>/IteratorExample?type=getDetails">Show Employee Details</a></strong>
<br></br>

<table cellspacing="2" cellpadding="2">

<tr><th>Employee ID</th><th>Employee Age</th><th>Employee Name</th><th>Employee City</th></tr>
<%
	// Iterating through subjectList

if(request.getAttribute("treasures") != null)  // Null check for the object
{
	Iterator<Artifacts> iterator = ad.iterator();  // Iterator interface
	
	while(iterator.hasNext())  // iterate through all the data until the last record
	{
		Artifacts treasureDetails = iterator.next(); //assign individual employee record to the employee class object
%>
	<tr><td><%=treasureDetails.getAid()%></td>
		<td><%=treasureDetails.getArtifact()%></td>
		<td><%=treasureDetails.getCategory()%></td>
		<td><%=treasureDetails.getEmail()%></td>
	</tr>
	<%
	}
}
%>
</table>

</body>
</html>
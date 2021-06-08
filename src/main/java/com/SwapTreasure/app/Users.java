package com.SwapTreasure.app;
import javax.persistence.Entity;
import javax.persistence.Id;


@Entity
public class Users {
	
	@Id
	private int uid;
	private String uname;
	private String pwd;
	private String fname;
	private String lname;
	private String email;
	private String dob;
	

	public String getUname() {
		return uname;
	}
	public void setUname(String uname) {
		this.uname = uname;
	}
	public String getPwd() {
		return pwd;
	}
	public void setPwd(String pwd) {
		this.pwd = pwd;
	}
	public String getFname() {
		return fname;
	}
	public void setFname(String fname) {
		this.fname = fname;
	}
	public String getLname() {
		return lname;
	}
	public void setLname(String lname) {
		this.lname = lname;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public String getDob() {
		return dob;
	}
	public void setDob(String dob) {
		this.dob = dob;
	}
	@Override
	public String toString() {
		return "Reg [uname=" + uname + ", pwd=" + pwd + ", fname=" + fname + ", lname=" + lname + ", email=" + email
				+ ", dob=" + dob + "]";
	}
	
	
}

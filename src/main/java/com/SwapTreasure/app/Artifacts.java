package com.SwapTreasure.app;

import javax.persistence.Entity;
import javax.persistence.Id;



@Entity
public class Artifacts {
	
	@Id
	private int aid;
	private String artifact;
	private String category;
	private int age;
	private String desc;
	private String contact;
	private int rid;
	
	
	public String getEmail() {
		return contact;
	}
	public void setEmail(String email) {
		this.contact = email;
	}
	public String getCategory() {
		return category;
	}
	public void setCategory(String category) {
		this.category = category;
	}
	public int getAid() {
		return aid;
	}
	public void setAid(int aid) {
		this.aid = aid;
	}
	public String getArtifact() {
		return artifact;
	}
	public void setArtifact(String artifact) {
		this.artifact = artifact;
	}
	public int getAge() {
		return age;
	}
	public void setAge(int age) {
		this.age = age;
	}
	public String getDesc() {
		return desc;
	}
	public void setDesc(String desc) {
		this.desc = desc;
	}
	@Override
	public String toString() {
		return "Ad [aid=" + aid + ", artifact=" + artifact + ", category=" + category + ", age=" + age + ", desc="
				+ desc + ", email=" + contact + "]";
	}
	
	
}

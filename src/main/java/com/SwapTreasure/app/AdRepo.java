package com.SwapTreasure.app;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.CrudRepository;
		//CRUDRepository
public interface AdRepo extends JpaRepository<Artifacts,Integer>{

	
}

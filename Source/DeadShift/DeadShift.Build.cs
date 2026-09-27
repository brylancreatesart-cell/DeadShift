// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class DeadShift : ModuleRules
{
	public DeadShift(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"DeadShift",
			"DeadShift/Variant_Platforming",
			"DeadShift/Variant_Platforming/Animation",
			"DeadShift/Variant_Combat",
			"DeadShift/Variant_Combat/AI",
			"DeadShift/Variant_Combat/Animation",
			"DeadShift/Variant_Combat/Gameplay",
			"DeadShift/Variant_Combat/Interfaces",
			"DeadShift/Variant_Combat/UI",
			"DeadShift/Variant_SideScrolling",
			"DeadShift/Variant_SideScrolling/AI",
			"DeadShift/Variant_SideScrolling/Gameplay",
			"DeadShift/Variant_SideScrolling/Interfaces",
			"DeadShift/Variant_SideScrolling/UI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}

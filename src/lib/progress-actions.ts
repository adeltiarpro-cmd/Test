"use server";

import { revalidatePath } from "next/cache";
import { createClient } from "@/lib/supabase/server";

export async function saveGoal(formData: FormData) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) throw new Error("Non authentifié");

  const targetDate = (formData.get("target_date") as string) || null;
  const dailyGoalRaw = formData.get("daily_goal") as string;
  const dailyGoal = dailyGoalRaw ? parseInt(dailyGoalRaw, 10) : null;

  await supabase
    .from("profiles")
    .update({ target_date: targetDate, daily_goal: dailyGoal })
    .eq("id", user.id);

  revalidatePath("/progress");
}
